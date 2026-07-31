import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.getenv("DATA_DIR", "/tmp/renomeador-danfe"))
SESSIONS_DIR = DATA_DIR / "sessoes"

SESSION_TTL_HOURS = int(os.getenv("SESSION_TTL_HOURS", "6"))
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "25"))
MAX_CONCURRENT_PROCESSING = max(1, int(os.getenv("MAX_CONCURRENT_PROCESSING", "3")))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Layout fixo informado pelo usuário.
BARCODE_DPI = int(os.getenv("BARCODE_DPI", "180"))
BARCODE_CROP = (0.48, 0.10, 1.00, 0.34)
OCR_DPI = int(os.getenv("OCR_DPI", "180"))
OCR_CROP = (0.68, 0.00, 1.00, 0.16)

SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
