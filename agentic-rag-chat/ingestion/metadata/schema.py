from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentMetadata(BaseModel):
    document_id: str
    source_path: str
    file_type: str
    chunk_id: Optional[int] = None
    language: Optional[str] = None
    version: int = 1
    created_at: datetime
    content_hash: str
