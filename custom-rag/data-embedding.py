from dotenv import load_dotenv
import os
import json
import pandas as pd
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from uuid import uuid4
import shutil
import time
import pdfplumber
import docx
from py_mini_racer import py_mini_racer  # Replacing js2py with py_mini_racer
from pathlib import Path

load_dotenv()

embeddings = OllamaEmbeddings(
    model=os.getenv("EMBEDDING_MODEL"),  # type: ignore
)

if os.path.exists(os.getenv("DATABASE_LOCATION")):  # type: ignore
    shutil.rmtree(os.getenv("DATABASE_LOCATION"))  # type: ignore

vector_store = Chroma(
    collection_name=os.getenv("COLLECTION_NAME"),  # type: ignore
    embedding_function=embeddings,
    persist_directory=os.getenv("DATABASE_LOCATION"),
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)

# Function to process different file types
def process_file(file_path):
    """Process various types of files and extract text."""
    ext = file_path.suffix.lower()

    if ext == ".txt":
        return process_txt_file(file_path)
    elif ext == ".pdf":
        return process_pdf_file(file_path)
    elif ext == ".docx":
        return process_docx_file(file_path)
    elif ext == ".py":
        return process_code_file(file_path)
    elif ext in {".js", ".jsx", ".ts", ".tsx"}:
        return process_code_file(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def process_txt_file(file_path):
    """Process a txt file."""
    with open(file_path, encoding="utf-8") as f:
        return f.read()

def process_pdf_file(file_path):
    """Process a pdf file."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def process_docx_file(file_path):
    """Process a docx file."""
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def process_code_file(file_path):
    """Process code files like .py, .js, .jsx, .ts, .tsx."""
    ext = file_path.suffix.lower()

    # If it's a JavaScript or TypeScript file, execute the code with py_mini_racer
    if ext in {".js", ".jsx", ".ts", ".tsx"}:
        with open(file_path, "r", encoding="utf-8") as file:
            js_code = file.read()

        js_vm = py_mini_racer.MiniRacer()
        try:
            result = js_vm.execute(js_code)  # Executes the JS code
            return result  # Returning the execution result (could be empty or undefined)
        except Exception as e:
            print(f"Error executing JS code in {file_path}: {e}")
            return ""
    else:
        # For .py or other code files, just return the text content
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

def process_all_files_in_folder(folder_path):
    """Process all files in the folder and return their text content."""
    texts = []
    for file_path in Path(folder_path).rglob("*"):  # Recursively go through all files
        if file_path.is_file():
            try:
                text = process_file(file_path)
                if text:  # If text was extracted
                    texts.append({"text": text, "source": str(file_path)})
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
    return texts


# Process all files in the folder (replace with your actual folder path)
folder_path = os.getenv("DATASET_STORAGE_FOLDER")  # type: ignore
file_content = process_all_files_in_folder(folder_path)

for line in file_content:
    print(f"Processing {line['source']}")

    texts = text_splitter.create_documents([line['text']], metadatas=[{"source": line['source']}])

    uuids = [str(uuid4()) for _ in range(len(texts))]

    vector_store.add_documents(documents=texts, ids=uuids)
