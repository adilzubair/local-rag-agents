from pydantic import BaseModel
from typing import Optional, Dict, Any

class Chunk(BaseModel):
    text: str
    metadata: Dict[str, Any]


class BaseChunker:
    def chunk(self, text: str, base_metadata: Dict[str, Any]) -> list[Chunk]:
        raise NotImplementedError
