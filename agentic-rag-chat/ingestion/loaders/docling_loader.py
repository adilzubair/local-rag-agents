from pathlib import Path
from docling.document_converter import DocumentConverter

class DoclingLoader:
    def __init__(self):
        self.converter = DocumentConverter()

    def load(self, file_path: Path) -> str:
        result = self.converter.convert(file_path)
        return result.document.export_to_text()
