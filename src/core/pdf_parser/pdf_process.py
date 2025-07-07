import os
from typing import List, Dict, Any

import pdfplumber
import pandas as pd

from src.core.utils.ocr import image_to_text
from src.core.utils.utils import get_uuid
from src.core.utils.table_parser import TableParser


class ParserPDF:
    """Simple PDF parser with OCR and table extraction."""

    def __init__(self):
        if not os.path.exists("data/cache/tables"):
            os.makedirs("data/cache/tables", exist_ok=True)
        self._table_parser = TableParser()

    def _extract_tables(self, page, structured: bool = False) -> List[Any]:
        """Extract tables as file paths or structured data."""
        tables = []
        for table in page.extract_tables():
            df = self._table_parser.to_dataframe(table)
            if structured:
                tables.append(self._table_parser.to_records(table))
            else:
                path = f"data/cache/tables/{get_uuid()}.xlsx"
                df.to_excel(path, index=False)
                tables.append(path)
        return tables

    def _extract_figures(self, page) -> str:
        """OCR text from images and charts on the page."""
        texts = []
        for img in page.images:
            try:
                extracted = page.extract_image(img["name"])
                if extracted:
                    texts.append(image_to_text(extracted["image"]))
            except Exception:
                continue
        return "\n".join([t for t in texts if t])

    def parse(self, pdf_path: str, structured: bool = False) -> List[Dict[str, Any]]:
        """Parse a PDF file into text, figure and table elements."""
        results = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                index = len(results)
                if text.strip():
                    results.append({"content": text.strip(), "style": "text", "index": index})
                ocr_text = self._extract_figures(page)
                if ocr_text:
                    results.append({"content": ocr_text, "style": "image", "index": len(results)})
                for tbl in self._extract_tables(page, structured=structured):
                    results.append({"content": tbl, "style": "tables", "index": len(results)})
        return results

    def main(self, state, structured: bool = False):
        """Entry point for workflow integration."""
        result = {}
        file_list = (
            state["input_files"] if isinstance(state["input_files"], list) else [state["input_files"]]
        )
        for file_path in file_list:
            result[file_path] = self.parse(file_path, structured=structured)
        return result
