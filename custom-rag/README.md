# Custom RAG Agent

This project implements a custom Retrieval-Augmented Generation (RAG) system with streaming support, allowing for real-time interaction with an AI agent.

## Features

- **Data Ingestion**: Embed local datasets into a ChromaDB vector store.
- **Streaming Chatbot**: Interactive CLI chatbot with streaming responses.
- **Local Persistence**: Uses ChromaDB for local vector storage.

## Project Structure

- `data-embedding.py`: Script to process datasets and create vector embeddings.
- `chatbot-stream.py`: The main chatbot interface with streaming output.
- `datasets/`: Directory containing source documents for the RAG system.
- `chroma_db/`: Local storage for vector embeddings.

## Installation

1. Navigate to this directory:
   ```bash
   cd custom-rag
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your environment:
   Create a `.env` file with your API keys (e.g., `OPENAI_API_KEY`).

## Usage

### 1. Embed Data
Run the embedding script to populate your vector store:
```bash
python data-embedding.py
```

### 2. Start Chatbot
Run the streaming chatbot:
```bash
python chatbot-stream.py
```

## License

MIT
