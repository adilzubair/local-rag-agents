import os
from langchain_chroma import Chroma
from vector_store.embeddings import EmbeddingModel
from ingestion.chunking.base import Chunk
from typing import List
from dotenv import load_dotenv
from langchain.schema import Document  # <-- important

load_dotenv()

class VectorStoreManager:
    def __init__(self, collection_name=None, persist_dir=None, embedding_model=None):
        self.collection_name = collection_name or os.getenv("COLLECTION_NAME")
        self.persist_dir = persist_dir or os.getenv("DATABASE_LOCATION")
        self.embedding_model = embedding_model or EmbeddingModel()
        
        # Initialize Chroma
        self.vector_store = Chroma(
            collection_name=self.collection_name,               # type: ignore
            embedding_function=self.embedding_model.model,
            persist_directory=self.persist_dir,
        )

    def add_chunks(self, chunks: List[Chunk]):
        """
        Converts chunks into LangChain Document objects before adding to Chroma.
        """
        documents = [
            Document(
                page_content=c.text,
                metadata=c.metadata
            )
            for c in chunks
        ]

        self.vector_store.add_documents(documents=documents)

    def similarity_search(self, query: str, k=5):
        return self.vector_store.similarity_search(query, k=k)
