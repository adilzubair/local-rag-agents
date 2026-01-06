from dotenv import load_dotenv
import os
import shutil
from uuid import uuid4
from pathlib import Path

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

from docling.document_converter import DocumentConverter
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

MAX_TOKENS = 512
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
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_MODEL)

chunker = HybridChunker(
    tokenizer=tokenizer,
    merge_peers=True,
)

# ==========================
# Ingestion Pipeline
# ==========================

def ingest_file(file_path: Path):
    print(f"Processing: {file_path}")

    result = converter.convert(str(file_path))
    doc = result.document

    chunks = chunker.chunk(dl_doc=doc)

    documents = []
    ids = []

    for chunk in chunks:
        text = chunker.contextualize(chunk)

        metadata = {
            "source": str(file_path),
            "page": getattr(chunk.meta, "page", None),
            "section": getattr(chunk.meta, "section_title", None),
            "doc_type": file_path.suffix,
        }

        documents.append(
            Document(page_content=text, metadata=metadata)
        )
        ids.append(str(uuid4()))

    vector_store.add_documents(documents=documents, ids=ids)

# ==========================
# Run Ingestion
# ==========================

for path in DATASET_FOLDER.rglob("*"):
    if path.is_file():
        try:
            ingest_file(path)
        except Exception as e:
            print(f"Failed to process {path}: {e}")

print("✓ Ingestion complete")
