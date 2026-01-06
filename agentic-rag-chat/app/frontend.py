import streamlit as st
import requests
import os
from pathlib import Path

# Configuration
BACKEND_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Agentic RAG Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for glassmorphism and modern look
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    .stSidebar {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    .chunk-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }
    .chunk-card:hover {
        transform: translateY(-2px);
        background: rgba(255, 255, 255, 0.08);
    }
    .source-label {
        font-size: 0.8rem;
        color: #94a3b8;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Agentic RAG Chat")
st.markdown("Upload files and query your knowledge base in real-time.")

# Sidebar - Ingestion
with st.sidebar:
    st.header("📂 Data Ingestion")
    uploaded_files = st.file_uploader("Choose documents to upload", accept_multiple_files=True)
    
    if uploaded_files:
        if st.button("🚀 Process & Ingest"):
            for uploaded_file in uploaded_files:
                with st.spinner(f"Ingesting {uploaded_file.name}..."):
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    try:
                        response = requests.post(f"{BACKEND_URL}/upload", files=files)
                        if response.status_code == 200:
                            data = response.json()
                            st.success(f"Ingested {data['chunks_added']} chunks from {uploaded_file.name}")
                        else:
                            st.error(f"Failed to ingest {uploaded_file.name}: {response.text}")
                    except Exception as e:
                        st.error(f"Connection Error: {e}")

    st.divider()
    st.info("Supported formats: .py, .md, .pdf, .docx, .txt")

# Main Interface - Querying
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "results" in message:
            with st.expander("🔍 View Retrieved Chunks"):
                for i, chunk in enumerate(message["results"]):
                    st.markdown(f"**Chunk {i+1}** ({chunk['metadata'].get('source_path', 'Unknown source')})")
                    st.code(chunk["content"])

# User prompt
if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/query", 
                    json={"query": prompt, "k": 3}
                )
                if response.status_code == 200:
                    data = response.json()
                    results = data["results"]
                    answer = data.get("answer", "No answer generated.")
                    
                    st.markdown(f"### 🤖 Agent Response\n{answer}")
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer,
                        "results": results
                    })
                    
                    if results:
                        with st.expander("🔍 View Retrieved Chunks"):
                            for i, chunk in enumerate(results):
                                st.markdown(f"**Chunk {i+1}** ({chunk['metadata'].get('source_path', 'Unknown source')})")
                                st.code(chunk["content"])
                    else:
                        st.info("No relevant chunks were found for this query.")
                else:
                    st.error(f"Query API Error: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
