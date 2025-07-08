from __future__ import annotations

"""Utilities for table-aware document chunking."""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Chunk:
    type: str
    content: Any
    page: int | None = None
    meta: Dict[str, Any] = field(default_factory=dict)


class TableAwareChunker:
    """Segment parsed document elements while respecting table boundaries."""

    def __init__(self, max_chars: int = 400):
        self.max_chars = max_chars

    def chunk(self, elements: List[Dict[str, Any]]) -> List[Chunk]:
        chunks: List[Chunk] = []
        buffer: List[str] = []
        page = None
        for elem in elements:
            elem_type = elem.get("type")
            if elem_type == "tables":
                if buffer:
                    chunks.append(Chunk(type="text", content=" ".join(buffer), page=page))
                    buffer = []
                chunks.append(Chunk(type="table", content=elem["content"], page=elem.get("page")))
                page = elem.get("page")
                continue

            text = elem.get("content", "")
            if page is None:
                page = elem.get("page")
            if len(" ".join(buffer)) + len(text) > self.max_chars:
                if buffer:
                    chunks.append(Chunk(type="text", content=" ".join(buffer), page=page))
                buffer = [text]
                page = elem.get("page")
            else:
                buffer.append(text)
                page = elem.get("page")
        if buffer:
            chunks.append(Chunk(type="text", content=" ".join(buffer), page=page))
        return chunks
