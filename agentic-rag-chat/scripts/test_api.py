import requests
import time
import os
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_root():
    response = requests.get(f"{BASE_URL}/")
    print(f"Root: {response.json()}")
    assert response.status_code == 200

def test_ingest():
    file_path = str(Path("datasets/cosigner1.py").absolute())
    response = requests.post(f"{BASE_URL}/ingest", json={"file_path": file_path})
    print(f"Ingest: {response.json()}")
    assert response.status_code == 200

def test_query():
    response = requests.post(f"{BASE_URL}/query", json={"query": "What is in cosigner1.py?", "k": 2})
    print(f"Query: {response.json()}")
    assert response.status_code == 200

if __name__ == "__main__":
    # Give the server a moment to start if needed
    try:
        test_root()
        test_ingest()
        test_query()
        print("API integration tests passed!")
    except Exception as e:
        print(f"Tests failed: {e}")
