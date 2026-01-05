from pathlib import Path
from ingestion.pipeline import ingest_and_index
from dotenv import load_dotenv

load_dotenv()

file_path = Path("datasets/script1.py")
num_chunks = ingest_and_index(file_path)
print(f"Added {num_chunks} chunks to vector store")
