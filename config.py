import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.getenv("DATA_DIR", "/tmp/renomeador-danfe"))
SESSIONS_DIR = DATA_DIR / "sessoes"

PDF_DPI = int(os.getenv("PDF_DPI", "150"))
OCR_MAX_WIDTH = int(os.getenv("OCR_MAX_WIDTH", "900"))
SESSION_TTL_HOURS = int(os.getenv("SESSION_TTL_HOURS", "6"))
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "25"))
MAX_CONCURRENT_OCR = max(1, int(os.getenv("MAX_CONCURRENT_OCR", "1")))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Recorte fixo da caixa NF-e / número / série no canto superior direito.
OCR_CROPS = (
    (0.68, 0.00, 1.00, 0.16),
)

SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
