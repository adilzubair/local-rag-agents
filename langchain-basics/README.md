# LangChain Basics

This project explores various fundamentals and advanced features of LangChain, from simple RAG systems to multi-modal agents and custom middleware.

## Features

- **Simple RAG**: Basic implementation of Retrieval-Augmented Generation.
- **Dynamic Model Selection**: Logic to switch between models based on constraints.
- **Custom Middleware**: Implementing custom processing layers for LLM interactions.
- **Multi-Modal Support**: Handling both text and image inputs within a single agent context.

## Project Structure

- `simple-rag.py`: A basic RAG implementation.
- `dynamic-model.py`: Demonstrates dynamic model selection logic.
- `middleware.py` & `custom-middleware.py`: Examples of custom middleware implementations.
- `multi-modal.py`: Multi-modal RAG example.
- `main.py`: Entry point for basic experiments.
- `pyproject.toml` & `uv.lock`: Dependency management using `uv`.

## Installation

1. Navigate to this directory:
   ```bash
   cd langchain-basics
   ```

2. Install dependencies (recommended to use `uv`):
   ```bash
   uv sync
   ```
   Or using pip:
   ```bash
   pip install .
   ```

3. Configure your environment:
   Ensure your `.env` file is populated with necessary API keys.

## Usage

You can run individual scripts to test different functionalities:
```bash
python simple-rag.py
python multi-modal.py
```

## License

MIT
