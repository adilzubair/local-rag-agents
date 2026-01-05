# Wiki RAG Agent

A specialized Retrieval-Augmented Generation (RAG) agent that sources its knowledge base from Wikipedia. This project includes scripts for data scraping, chunking, embedding, and a terminal-based chatbot.

## Features

- **Wikipedia Scraping**: Automated data extraction from Wikipedia articles.
- **Efficient Chunking**: Intelligent text splitting for better retrieval context.
- **Vector Search**: Uses embeddings and vector storage for similarity-based retrieval.
- **Interactive Chat**: A CLI chatbot interface for querying the scraped data.

## Project Structure

- `scraping-wiki.py`: Scrapes text data from specified Wikipedia URLs.
- `chunking_embedding_ingestion.py`: Processes scraped data into chunks and embeds them.
- `chatbot.py`: Interactive chatbot CLI.
- `keywords.xlsx`: Configurable list of keywords or topics to scrape.
- `chroma_db/`: Local vector database storage.

## Installation

1. Navigate to this directory:
   ```bash
   cd wiki-rag
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your environment:
   Populate your `.env` file with necessary API keys.

## Usage

### 1. Scrape Knowledge Base
Run the scraper (uses `keywords.xlsx` or hardcoded sources):
```bash
python scraping-wiki.py
```

### 2. Ingest Data
Process and embed the scraped data:
```bash
python chunking_embedding_ingestion.py
```

### 3. Query the Agent
Start the chatbot:
```bash
python chatbot.py
```

## License

MIT
