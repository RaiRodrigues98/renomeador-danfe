import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data"))
SESSIONS_DIR = DATA_DIR / "sessoes"
LOG_DIR = DATA_DIR / "logs"

# Renderização apenas do recorte superior direito do DANFE.
PDF_DPI = int(os.getenv("PDF_DPI", "220"))
CROP_X1 = float(os.getenv("CROP_X1", "0.58"))
CROP_Y1 = float(os.getenv("CROP_Y1", "0.00"))
CROP_X2 = float(os.getenv("CROP_X2", "1.00"))
CROP_Y2 = float(os.getenv("CROP_Y2", "0.20"))

# Sessões antigas são removidas automaticamente.
SESSION_TTL_HOURS = int(os.getenv("SESSION_TTL_HOURS", "12"))
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "25"))

SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
