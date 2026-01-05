from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    # Models
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    chat_model: str = os.getenv("CHAT_MODEL", "llama3")
    model_provider: str = os.getenv("MODEL_PROVIDER", "ollama")

    # Vector DB
    collection_name: str = os.getenv("COLLECTION_NAME", "rag_docs")
    persist_directory: str = os.getenv("DATABASE_LOCATION", "./chroma")

    # Ingestion
    dataset_folder: str = os.getenv("DATASET_STORAGE_FOLDER", "./data")

    # Retrieval
    top_k: int = int(os.getenv("TOP_K", 5))

settings = Settings()
