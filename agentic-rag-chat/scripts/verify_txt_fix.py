from pathlib import Path
from ingestion.pipeline import ingest_and_index
from dotenv import load_dotenv
import os

load_dotenv()

# Ensure we are in the right directory if needed or use absolute paths
# But since we run from root, relative should work if uploads/ exists
file_path = Path("uploads/test_ingestion.txt")

try:
    num_chunks = ingest_and_index(file_path)
    print(f"SUCCESS: Added {num_chunks} chunks for {file_path}")
except Exception as e:
    print(f"FAILURE: {e}")
