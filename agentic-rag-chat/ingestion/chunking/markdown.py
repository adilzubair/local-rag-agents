import re
from ingestion.chunking.base import BaseChunker, Chunk

HEADER_REGEX = re.compile(r"^(#{1,6})\s+(.*)", re.MULTILINE)

class MarkdownChunker(BaseChunker):
    def __init__(self, max_chars: int = 1200):
        self.max_chars = max_chars

    def chunk(self, text: str, base_metadata: dict) -> list[Chunk]:
        sections = []
        matches = list(HEADER_REGEX.finditer(text))

        if not matches:
            sections = [("No Header", text.strip())]
        else:
            for i, match in enumerate(matches):
                start = match.start()
                end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

                header = match.group(2)
                section_text = text[start:end].strip()

                sections.append((header, section_text))

        chunks: list[Chunk] = []
        chunk_id = 0

        for header, section in sections:
            if len(section) <= self.max_chars:
                chunks.append(
                    Chunk(
                        text=section,
                        metadata={
                            **base_metadata,
                            "chunk_id": chunk_id,
                            "section": header,
                            "type": "document"
                        }
                    )
                )
                chunk_id += 1
            else:
                # Fallback: split large sections
                for i in range(0, len(section), self.max_chars):
                    part = section[i:i + self.max_chars]
                    chunks.append(
                        Chunk(
                            text=part,
                            metadata={
                                **base_metadata,
                                "chunk_id": chunk_id,
                                "section": header,
                                "type": "document"
                            }
                        )
                    )
                    chunk_id += 1

        return chunks
