import os
import shutil
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Body, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ingestion.pipeline import ingest_and_index
from vector_store.manager import VectorStoreManager
from app.llm import LLMService
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Agentic RAG Chat API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure upload directory exists
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Initialize Vector Store Manager
try:
    vector_store_manager = VectorStoreManager()
except Exception as e:
    print(f"Warning: Could not initialize VectorStoreManager: {e}")
    vector_store_manager = None

# Initialize LLM Service
try:
    llm_service = LLMService()
except Exception as e:
    print(f"Warning: Could not initialize LLMService: {e}")
    llm_service = None

class IngestRequest(BaseModel):
    file_path: str

class QueryRequest(BaseModel):
    query: str
    k: Optional[int] = 5

class ChunkResponse(BaseModel):
    content: str
    metadata: dict

class QueryResponse(BaseModel):
    answer: str
    results: List[ChunkResponse]

@app.get("/")
async def root():
    return {"message": "Welcome to Agentic RAG Chat API"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = UPLOAD_DIR / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        num_chunks = ingest_and_index(file_path, vector_store_manager=vector_store_manager)
        return {
            "message": f"Successfully uploaded and ingested {file.filename}",
            "chunks_added": num_chunks,
            "file_path": str(file_path)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/ingest")
async def ingest_file_endpoint(request: IngestRequest):
    path = Path(request.file_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {request.file_path}")
    
    try:
        num_chunks = ingest_and_index(path, vector_store_manager=vector_store_manager)
        return {"message": f"Successfully ingested {num_chunks} chunks", "chunks_added": num_chunks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    if not vector_store_manager:
        raise HTTPException(status_code=500, detail="Vector store not initialized")
    
    try:
        # 1. Similarity search
        docs = vector_store_manager.similarity_search(request.query, k=request.k)
        
        # 2. Extract results for response
        results = [
            ChunkResponse(content=doc.page_content, metadata=doc.metadata)
            for doc in docs
        ]
        
        # 3. Generate answer using LLM
        answer = "No LLM service available to generate an answer."
        if llm_service:
            answer = llm_service.generate_response(request.query, docs)
            
        return QueryResponse(answer=answer, results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
