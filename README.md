# 🤖 Local RAG Agents

A comprehensive collection of local **Retrieval-Augmented Generation (RAG)** agents and architectures built with **LangChain**, **FastAPI**, **Streamlit**, and **Python**. This repository serves as a playground for exploring modern RAG pipelines, from simple document ingestion to complex agentic workflows.

---

## 🚀 Projects

Each project is self-contained within its own directory, featuring its own environment configuration and specialized implementation.

### 🧠 Agentic & Advanced RAG
- **[agentic-rag-chat](./agentic-rag-chat)**: A high-performance, modular RAG system with a FastAPI backend and Streamlit frontend. Features smart semantic chunking and a robust vector search pipeline using ChromaDB.
- **[docling-rag-agent](./docling-rag-agent)**: An advanced RAG agent utilizing **Docling** for sophisticated multi-format document parsing (PDF, DOCX, MD, TXT) and **LangGraph** for structured reasoning and tool usage.

### 🛠️ Foundations & Patterns
- **[custom-rag](./custom-rag)**: A clean implementation of a streaming chatbot with a custom data embedding and retrieval pipeline.
- **[langchain-basics](./langchain-basics)**: A laboratory for LangChain fundamentals, including dynamic model selection, custom middleware, and multi-modal capabilities.
- **[wiki-rag](./wiki-rag)**: An automated system that scrapes Wikipedia data, performs chunking/embedding, and provides an interactive chatbot interface.

---

## 🛠️ Tech Stack & Tools

- **Frameworks**: [LangChain](https://github.com/langchain-ai/langchain), [LangGraph](https://github.com/langchain-ai/langgraph), [FastAPI](https://fastapi.tiangolo.com/)
- **Frontend**: [Streamlit](https://streamlit.io/)
- **Vector Database**: [ChromaDB](https://www.trychroma.com/)
- **Parsing**: [Docling](https://github.com/DS4SD/docling)
- **Dependency Management**: [uv](https://github.com/astral-sh/uv)

---

## 🏁 Getting Started

### Prerequisites
- **Python 3.10+** (Recommended 3.13)
- **[uv](https://github.com/astral-sh/uv)**: The recommended package manager for this repository.

### Quick Setup
1. **Navigate to a project**:
   ```bash
   cd agentic-rag-chat
   ```
2. **Install dependencies**:
   ```bash
   uv sync
   ```
3. **Follow the specific instructions** in the project's `README.md`.

---

## 📄 License
MIT
