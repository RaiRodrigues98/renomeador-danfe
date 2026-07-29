from pathlib import Path

BASE_DIR = Path(__file__).parent

UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
LOG_DIR = BASE_DIR / "logs"

POPPLER_PATH = BASE_DIR / "poppler" / "Library" / "bin"
TESSERACT_PATH = BASE_DIR / "Tesseract-OCR" / "tesseract.exe"

PDF_DPI = 300
OCR_LANGUAGE = "por"

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)