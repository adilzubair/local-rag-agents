from pathlib import Path

class CodeLoader:
    """Load code files safely as text for chunking."""
    
    SUPPORTED_EXTENSIONS = {".py", ".js", ".ts", ".jsx", ".tsx"}

    def load(self, file_path: Path) -> str:
        if file_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported code file: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
