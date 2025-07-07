# -*- coding: utf-8 -*-
"""Unified document parser and semantic splitter utilities."""
from __future__ import annotations

import logging
import os
from typing import Dict, List, Any

import pandas as pd

from .docx_parser.docx_process import ParserDocx
from .pdf_parser.pdf_process import ParserPDF
from .models.semantic_splitter import SemanticParagraphSplitter
from .models.embeddings import Embedding

logger = logging.getLogger(__name__)


class DocumentParser:
    """Parse docx and pdf files into structured text and table data."""

    def __init__(self) -> None:
        self._docx = ParserDocx()
        self._pdf = ParserPDF()

    def _load_table(self, path: str) -> List[Dict[str, Any]]:
        """Read an Excel table produced during parsing into a list of rows."""
        try:
            df = pd.read_excel(path)
            return df.to_dict(orient="records")
        except Exception:  # pragma: no cover - best effort loading
            logger.exception("Failed to load table: %s", path)
            return []

    def parse_docx(self, file_path: str) -> Dict[str, Any]:
        """Parse a docx file and return text blocks and table structures."""
        result = {"text": [], "tables": []}
        try:
            for item in self._docx.read2docx(file_path):
                if item.get("type") == "tables":
                    result["tables"].append(self._load_table(item["content"]))
                else:
                    result["text"].append(item["content"])
        except Exception as exc:  # pragma: no cover - input may be invalid
            logger.exception("docx parsing failed: %s", exc)
            result["error"] = str(exc)
        return result

    def parse_pdf(self, file_path: str) -> Dict[str, Any]:
        """Parse a PDF file extracting text and table information."""
        result = {"text": [], "tables": []}
        try:
            for item in self._pdf.parse(file_path):
                style = item.get("style")
                if style == "tables":
                    result["tables"].append(self._load_table(item["content"]))
                else:
                    result["text"].append(item["content"])
        except Exception as exc:  # pragma: no cover - input may be invalid
            logger.exception("pdf parsing failed: %s", exc)
            result["error"] = str(exc)
        return result


class SemanticSplitter:
    """Split text into semantically coherent passages."""

    def __init__(self, buffer_size: int = 1, threshold: int = 80, model: Any | None = None) -> None:
        model = model or Embedding()
        self._splitter = SemanticParagraphSplitter(model=model, buffer_size=buffer_size, threshold=threshold)

    def split(self, text: str) -> List[str]:
        return self._splitter.split_passages(text)


def ingest_document(file_path: str) -> Dict[str, Any]:
    """Example workflow that parses a document and splits its text."""
    parser = DocumentParser()
    splitter = SemanticSplitter()
    ext = os.path.splitext(file_path)[1].lower()

    if ext in {".doc", ".docx"}:
        parsed = parser.parse_docx(file_path)
    elif ext == ".pdf":
        parsed = parser.parse_pdf(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    paragraphs: List[str] = []
    for text in parsed.get("text", []):
        paragraphs.extend(splitter.split(text))

    return {"paragraphs": paragraphs, "tables": parsed.get("tables", [])}


if __name__ == "__main__":  # pragma: no cover - manual example
    docx_example = os.path.join("data", "docx2", "AF-folder", "AF01.docx")
    pdf_example = os.path.join("data", "pdf", "AF01.pdf")

    for path in (docx_example, pdf_example):
        res = ingest_document(path)
        print(f"=== Results for {os.path.basename(path)} ===")
        print("Paragraphs:")
        for p in res["paragraphs"]:
            print(f"- {p[:60]}")
        print("Tables:", res["tables"])
        print()
