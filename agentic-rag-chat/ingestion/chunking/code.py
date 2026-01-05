import ast
from ingestion.chunking.base import BaseChunker, Chunk

class PythonCodeChunker(BaseChunker):
    def chunk(self, text: str, base_metadata: dict) -> list[Chunk]:
        tree = ast.parse(text)
        chunks = []
        chunk_id = 0

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                start_line = node.lineno - 1
                end_line = node.end_lineno

                lines = text.splitlines()
                code_block = "\n".join(lines[start_line:end_line])

                chunks.append(
                    Chunk(
                        text=code_block,
                        metadata={
                            **base_metadata,
                            "chunk_id": chunk_id,
                            "symbol": node.name,
                            "type": "code",
                            "language": "python"
                        }
                    )
                )
                chunk_id += 1

        return chunks
