from pathlib import Path

class TextLoader:
    """Load plain text files."""

    def load(self, file_path: Path) -> str:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
