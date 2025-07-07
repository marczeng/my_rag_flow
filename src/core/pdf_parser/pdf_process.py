import os
from typing import List, Dict, Any

import pdfplumber
import pandas as pd

from src.core.utils.ocr import image_to_text
from src.core.utils.utils import get_uuid


class ParserPDF:
    """Simple PDF parser with OCR and table extraction."""

    def __init__(self):
        if not os.path.exists("data/cache/tables"):
            os.makedirs("data/cache/tables", exist_ok=True)

    def _extract_tables(self, page) -> List[str]:
        paths = []
        for table in page.extract_tables():
            df = pd.DataFrame(table[1:], columns=table[0])
            path = f"data/cache/tables/{get_uuid()}.xlsx"
            df.to_excel(path, index=False)
            paths.append(path)
        return paths

    def _extract_images(self, page) -> str:
        texts = []
        for img in page.images:
            try:
                extracted = page.extract_image(img["name"])
                if extracted:
                    texts.append(image_to_text(extracted["image"]))
            except Exception:
                continue
        return "\n".join([t for t in texts if t])

    def parse(self, pdf_path: str) -> List[Dict[str, Any]]:
        results = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text() or ""
                index = len(results)
                if text.strip():
                    results.append({"content": text.strip(), "style": "text", "index": index})
                ocr_text = self._extract_images(page)
                if ocr_text:
                    results.append({"content": ocr_text, "style": "image", "index": len(results)})
                for tbl_path in self._extract_tables(page):
                    results.append({"content": tbl_path, "style": "tables", "index": len(results)})
        return results

    def main(self, state):
        result = {}
        file_list = state["input_files"] if isinstance(state["input_files"], list) else [state["input_files"]]
        for file_path in file_list:
            result[file_path] = self.parse(file_path)
        return result
