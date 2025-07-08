import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.models.structured_chunker import TableAwareChunker


def test_table_aware_chunker():
    elements = [
        {"type": "content", "content": "A" * 50, "page": 1},
        {"type": "tables", "content": [["A"]], "page": 1},
        {"type": "content", "content": "B" * 50, "page": 1},
    ]
    chunker = TableAwareChunker(max_chars=60)
    chunks = chunker.chunk(elements)
    assert len(chunks) == 3
    assert chunks[1].type == "table"
