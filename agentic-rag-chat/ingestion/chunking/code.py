import ast
from ingestion.chunking.base import BaseChunker, Chunk

class PythonCodeChunker(BaseChunker):
    def chunk(self, text: str, base_metadata: dict) -> list[Chunk]:
        try:
            tree = ast.parse(text)
        except SyntaxError:
            # Fallback for broken python code
            return [Chunk(text=text, metadata={**base_metadata, "type": "code", "chunk_id": 0})]
            
        chunks = []
        chunk_id = 0
        lines = text.splitlines()
        last_line = 0

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                start_line = node.lineno - 1
                end_line = node.end_lineno

                # Capture any code BEFORE this block
                if start_line > last_line:
                    pre_block = "\n".join(lines[last_line:start_line]).strip()
                    if pre_block:
                        chunks.append(
                            Chunk(
                                text=pre_block,
                                metadata={
                                    **base_metadata,
                                    "chunk_id": chunk_id,
                                    "type": "code_context",
                                    "language": "python"
                                }
                            )
                        )
                        chunk_id += 1

                # Capture the block itself
                code_block = "\n".join(lines[start_line:end_line])
                chunks.append(
                    Chunk(
                        text=code_block,
                        metadata={
                            **base_metadata,
                            "chunk_id": chunk_id,
                            "symbol": getattr(node, "name", "unknown"),
                            "type": "code_block",
                            "language": "python"
                        }
                    )
                )
                chunk_id += 1
                last_line = end_line

        # Capture any remaining code
        if last_line < len(lines):
            post_block = "\n".join(lines[last_line:]).strip()
            if post_block:
                chunks.append(
                    Chunk(
                        text=post_block,
                        metadata={
                            **base_metadata,
                            "chunk_id": chunk_id,
                            "type": "code_context",
                            "language": "python"
                        }
                    )
                )

        # If no chunks were created (e.g. only top-level code), return the whole file
        if not chunks:
            chunks.append(
                Chunk(
                    text=text,
                    metadata={
                        **base_metadata,
                        "chunk_id": 0,
                        "type": "code",
                        "language": "python"
                    }
                )
            )

        return chunks
