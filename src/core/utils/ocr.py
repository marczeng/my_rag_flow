import os
from io import BytesIO
from PIL import Image
try:
    import pytesseract
except Exception:  # pragma: no cover - optional dependency
    pytesseract = None
from .utils import get_uuid


def image_to_text(image_bytes: bytes) -> str:
    """Extract text from image bytes using tesseract OCR."""
    if not os.path.exists("data/cache/images"):
        os.makedirs("data/cache/images")
    img_path = f"data/cache/images/{get_uuid()}.png"
    with open(img_path, "wb") as f:
        f.write(image_bytes)
    try:
        if pytesseract is None:  # pragma: no cover - optional dependency
            raise RuntimeError("pytesseract not installed")
        text = pytesseract.image_to_string(Image.open(img_path))
    except Exception:
        text = ""
    return text.strip()
