from dotenv import load_dotenv
import os
import shutil
from uuid import uuid4
from pathlib import Path
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
from transformers import AutoTokenizer

load_dotenv()

# ==========================
# Configuration
# ==========================
DATASET_FOLDER = Path(os.getenv("DATASET_STORAGE_FOLDER") or '')
VECTOR_DB_DIR = os.getenv("DATABASE_LOCATION")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
MAX_TOKENS = 256  # smaller chunks to avoid exceeding model context
TOKENIZER_MODEL = "BAAI/bge-large-en-v1.5"

# ==========================
# Vector Store Setup
# ==========================
embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL or '')

if os.path.exists(VECTOR_DB_DIR or ''):
    shutil.rmtree(VECTOR_DB_DIR or '')

vector_store = Chroma(
    collection_name=COLLECTION_NAME or '',
    embedding_function=embeddings,
    persist_directory=VECTOR_DB_DIR,
)

# ==========================
# Docling Setup
# ==========================
converter = DocumentConverter()

# Load tokenizer and modify its model_max_length
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_MODEL)
# Override the model_max_length to our desired MAX_TOKENS
tokenizer.model_max_length = MAX_TOKENS

chunker = HybridChunker(
    tokenizer=tokenizer,
    merge_peers=True,
)

# ==========================
# Helper functions
# ==========================
def ingest_file(file_path: Path):
    """Ingest a single file into Chroma vector DB."""
    print(f"Processing: {file_path}")
    
    try:
        # Handle .txt files separately by reading them directly
        if file_path.suffix.lower() == ".txt":
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Create a simple document for .txt files
            # Split into manageable chunks using the tokenizer
            tokens = tokenizer.encode(text)
            chunk_size = MAX_TOKENS
            
            documents = []
            ids = []
            
            for i in range(0, len(tokens), chunk_size):
                chunk_tokens = tokens[i:i + chunk_size]
                chunk_text = tokenizer.decode(chunk_tokens)
                
                if not chunk_text.strip():
                    continue
                
                metadata = {
                    "source": str(file_path),
                    "chunk_index": i // chunk_size,
                    "doc_type": file_path.suffix,
                }
                
                documents.append(Document(page_content=chunk_text, metadata=metadata))
                ids.append(str(uuid4()))
            
            if documents:
                vector_store.add_documents(documents=documents, ids=ids)
                print(f"✓ Added {len(documents)} chunks from {file_path.name}")
        
        else:
            # Use Docling for other formats (PDF, DOCX, MD)
            result = converter.convert(str(file_path))
            doc = result.document
            
            # Chunk and contextualize
            chunks = chunker.chunk(dl_doc=doc)
            documents = []
            ids = []
            
            for chunk in chunks:
                text = chunker.contextualize(chunk)
                if not text.strip():
                    continue  # skip empty chunks
                
                # Verify chunk doesn't exceed token limit
                tokens = tokenizer.encode(text)
                if len(tokens) > MAX_TOKENS:
                    # Split oversized chunk
                    for i in range(0, len(tokens), MAX_TOKENS):
                        sub_tokens = tokens[i:i + MAX_TOKENS]
                        sub_text = tokenizer.decode(sub_tokens)
                        
                        if not sub_text.strip():
                            continue
                        
                        metadata = {
                            "source": str(file_path),
                            "page": getattr(chunk.meta, "page", None),
                            "section": getattr(chunk.meta, "section_title", None),
                            "doc_type": file_path.suffix,
                            "sub_chunk": i // MAX_TOKENS,
                        }
                        
                        documents.append(Document(page_content=sub_text, metadata=metadata))
                        ids.append(str(uuid4()))
                else:
                    metadata = {
                        "source": str(file_path),
                        "page": getattr(chunk.meta, "page", None),
                        "section": getattr(chunk.meta, "section_title", None),
                        "doc_type": file_path.suffix,
                    }
                    
                    documents.append(Document(page_content=text, metadata=metadata))
                    ids.append(str(uuid4()))
            
            if documents:
                vector_store.add_documents(documents=documents, ids=ids)
                print(f"✓ Added {len(documents)} chunks from {file_path.name}")
                
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

# ==========================
# Run Ingestion
# ==========================
for path in DATASET_FOLDER.rglob("*"):
    if path.is_file() and path.suffix.lower() in {".pdf", ".docx", ".txt", ".md"}:
        ingest_file(path)

# Sanity check
doc_count = vector_store._collection.count()
print("\n✓ Ingestion complete")
print(f"Vector DB document count: {doc_count}")