import os
import sys
import docx
from PIL import Image, ImageDraw
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.docx_parser.docx_process import ParserDocx


def create_doc_with_image(path, img_path):
    doc = docx.Document()
    doc.add_picture(img_path)
    doc.save(path)


def create_image(path):
    img = Image.new("RGB", (200, 50), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), "Hello", fill="black")
    img.save(path)


def test_image_extraction(tmp_path):
    img_file = tmp_path / "hello.png"
    create_image(str(img_file))
    doc_file = tmp_path / "img.docx"
    create_doc_with_image(str(doc_file), str(img_file))

    parser = ParserDocx()
    with patch("src.core.utils.ocr.image_to_text", return_value="Hello"), \
         patch("src.core.docx_parser.docx_process.ocr_image_to_text", return_value="Hello"):
        result = parser.read2docx(str(doc_file))
    image_texts = [r["content"] for r in result if r.get("style") == "image"]
    assert any("hello" in txt.lower() for txt in image_texts)
