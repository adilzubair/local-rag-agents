from pathlib import Path
from ingestion.chunking.markdown import MarkdownChunker
from ingestion.chunking.code import PythonCodeChunker
from ingestion.loaders.code_loader import CodeLoader

def get_chunker_and_loader(file_path: Path):
    suffix = file_path.suffix.lower()

    # Code files
    if suffix in {".py", ".js", ".ts", ".jsx", ".tsx"}:
        return PythonCodeChunker(), CodeLoader()

    # Document files
    if suffix == ".txt":
        from ingestion.loaders.text_loader import TextLoader
        return MarkdownChunker(), TextLoader()

    if suffix in {".md", ".pdf", ".docx"}:
        from ingestion.loaders.docling_loader import DoclingLoader
        return MarkdownChunker(), DoclingLoader()

    # Fallback
    from ingestion.loaders.docling_loader import DoclingLoader
    return MarkdownChunker(), DoclingLoader()
