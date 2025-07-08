import os
import sys
from shutil import copyfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.pdf_parser.pdf_process import ParserPDF


def test_pdf_page_numbers(tmp_path):
    sample = os.path.join("data", "pdf", "AF01.pdf")
    target = tmp_path / "sample.pdf"
    copyfile(sample, target)
    parser = ParserPDF()
    res = parser.parse(str(target), structured=True)
    assert res
    assert all("page" in r for r in res)
