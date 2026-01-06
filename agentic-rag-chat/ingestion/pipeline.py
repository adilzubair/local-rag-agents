from pathlib import Path
from ingestion.chunking.factory import get_chunker_and_loader
from ingestion.metadata.schema import DocumentMetadata
from hashlib import sha256
from uuid import uuid4
from datetime import datetime, timezone

# --- Existing ingestion pipeline ---
def ingest_file(file_path: Path):
    """
    Ingest a file (document or code), chunk it, and return the chunks.
    """
    chunker, loader = get_chunker_and_loader(file_path)

    text = loader.load(file_path)
    content_hash = sha256(text.encode("utf-8")).hexdigest()

    metadata_obj = DocumentMetadata(
        document_id=str(uuid4()),
        source_path=str(file_path),
        file_type=file_path.suffix.lower(),
        created_at=datetime.now(timezone.utc),
        content_hash=content_hash
    )
    
    # Convert to dict and handle non-serializable types for Chroma
    base_metadata = metadata_obj.model_dump()
    base_metadata["created_at"] = base_metadata["created_at"].isoformat()

    chunks = chunker.chunk(text, base_metadata)
    return chunks


# --- New helper for production-ready indexing ---
def ingest_and_index(file_path: Path, vector_store_manager=None):
    """
    Ingest a file and add its chunks to the vector store.
    Returns the number of chunks added.
    """
    from vector_store.manager import VectorStoreManager

    chunks = ingest_file(file_path)
    
    # Use provided manager or create a default one
    manager = vector_store_manager or VectorStoreManager()
    manager.add_chunks(chunks)
    
    return len(chunks)
