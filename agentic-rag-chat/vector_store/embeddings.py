import os
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

class EmbeddingModel:
    def __init__(self, model_name=None, provider="ollama"):
        self.provider = provider.lower()
        self.model_name = model_name or os.getenv("EMBEDDING_MODEL")

        if self.provider == "ollama":
            self.model = OllamaEmbeddings(model=self.model_name)        #type: ignore
        elif self.provider == "openai":
            self.model = OpenAIEmbeddings(model=self.model_name)        #type: ignore
        else:
            raise ValueError(f"Unsupported embedding provider: {provider}")

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of texts."""
        return self.model.embed_documents(texts)
