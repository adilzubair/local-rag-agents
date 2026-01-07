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

# Modern, clean CSS with elegant design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #0a0a0a;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111111 0%, #0a0a0a 100%);
        border-right: 1px solid #1f1f1f;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }

    /* Header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 0%, #a0a0a0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    .sub-header {
        color: #707070;
        font-size: 1rem;
        font-weight: 400;
        margin-bottom: 3rem;
    }

    /* Chat messages */
    .stChatMessage {
        background: transparent !important;
        border: none !important;
        padding: 1.5rem 0 !important;
    }

    .stChatMessage[data-testid="user-message"] {
        background: transparent !important;
    }

    .stChatMessage[data-testid="assistant-message"] {
        background: transparent !important;
    }

    .stChatMessage [data-testid="chatAvatarIcon-user"] {
        background: #ffffff;
        color: #0a0a0a;
    }

    .stChatMessage [data-testid="chatAvatarIcon-assistant"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: #ffffff;
    }

    /* Message content */
    .stChatMessage p {
        color: #e0e0e0;
        line-height: 1.6;
        font-size: 0.95rem;
    }

    /* Source cards */
    .source-card {
        background: #111111;
        border: 1px solid #1f1f1f;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        transition: all 0.2s ease;
    }

    .source-card:hover {
        border-color: #2f2f2f;
        background: #141414;
    }

    .source-header {
        color: #8b5cf6;
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .source-path {
        color: #606060;
        font-size: 0.8rem;
        margin-bottom: 0.75rem;
        font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
    }

    .source-content {
        background: #0a0a0a;
        border: 1px solid #1a1a1a;
        border-radius: 6px;
        padding: 0.875rem;
        color: #c0c0c0;
        font-size: 0.875rem;
        line-height: 1.5;
        font-family: 'SF Mono', 'Monaco', 'Consolas', monospace;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 0.625rem 1.25rem;
        font-weight: 500;
        font-size: 0.875rem;
        transition: all 0.2s ease;
        width: 100%;
    }

    .stButton > button:hover {
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
        transform: translateY(-1px);
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #111111;
        border: 1px dashed #2f2f2f;
        border-radius: 8px;
        padding: 1.5rem;
    }

    [data-testid="stFileUploader"] label {
        color: #e0e0e0;
        font-size: 0.875rem;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #111111;
        border: 1px solid #1f1f1f;
        border-radius: 8px;
        color: #e0e0e0;
        font-weight: 500;
        font-size: 0.9rem;
    }

    .streamlit-expanderHeader:hover {
        border-color: #2f2f2f;
        background: #141414;
    }

    .streamlit-expanderContent {
        background: transparent;
        border: none;
    }

    /* Chat input */
    .stChatInputContainer {
        border-top: 1px solid #1f1f1f;
        background: #0a0a0a;
    }

    .stChatInput textarea {
        background: #111111 !important;
        border: 1px solid #1f1f1f !important;
        border-radius: 8px !important;
        color: #e0e0e0 !important;
        font-size: 0.95rem !important;
    }

    .stChatInput textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 1px #6366f1 !important;
    }

    /* Info boxes */
    .stAlert {
        background: #111111;
        border: 1px solid #1f1f1f;
        border-radius: 8px;
        color: #c0c0c0;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #6366f1 !important;
    }

    /* Divider */
    hr {
        border-color: #1f1f1f;
        margin: 1.5rem 0;
    }

    /* Success/Error messages */
    .stSuccess {
        background: #0f1f0f;
        border: 1px solid #1f3f1f;
        color: #7fdf7f;
    }

    .stError {
        background: #1f0f0f;
        border: 1px solid #3f1f1f;
        color: #ff7f7f;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">Agentic RAG</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Intelligent document retrieval powered by AI</p>', unsafe_allow_html=True)

# Sidebar - Ingestion
with st.sidebar:
    st.header("📁 Documents")
    uploaded_files = st.file_uploader("Upload your documents", accept_multiple_files=True, label_visibility="collapsed")

    if uploaded_files:
        if st.button("Process Documents"):
            for uploaded_file in uploaded_files:
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    try:
                        response = requests.post(f"{BACKEND_URL}/upload", files=files)
                        if response.status_code == 200:
                            data = response.json()
                            st.success(f"✓ Added {data['chunks_added']} chunks from {uploaded_file.name}")
                        else:
                            st.error(f"Failed to process {uploaded_file.name}")
                    except Exception as e:
                        st.error(f"Connection error: {e}")

    st.divider()
    st.info("Supported: .py, .md, .pdf, .docx, .txt")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "results" in message and message["results"]:
            with st.expander(f"📚 {len(message['results'])} sources retrieved"):
                for i, chunk in enumerate(message["results"]):
                    source = chunk['metadata'].get('source_path', 'Unknown source')
                    st.markdown(f"""
                    <div class="source-card">
                        <div class="source-header">Source {i+1}</div>
                        <div class="source-path">{source}</div>
                        <div class="source-content">{chunk['content']}</div>
                    </div>
                    """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Ask anything about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Prepare conversation history
                history = [
                    {"role": m["role"], "content": m["content"]} 
                    for m in st.session_state.messages[:-1]
                ]

                response = requests.post(
                    f"{BACKEND_URL}/query", 
                    json={
                        "query": prompt, 
                        "k": 3,
                        "history": history
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results = data["results"]
                    answer = data.get("answer", "No answer generated.")

                    st.markdown(answer)

                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer,
                        "results": results
                    })

                    if results:
                        with st.expander(f"📚 {len(results)} sources retrieved"):
                            for i, chunk in enumerate(results):
                                source = chunk['metadata'].get('source_path', 'Unknown source')
                                st.markdown(f"""
                                <div class="source-card">
                                    <div class="source-header">Source {i+1}</div>
                                    <div class="source-path">{source}</div>
                                    <div class="source-content">{chunk['content']}</div>
                                </div>
                                """, unsafe_allow_html=True)
                else:
                    st.error(f"Query failed: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")