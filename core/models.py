from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class ResultadoProcessamento:
    arquivo_original: str
    arquivo_final: Optional[str] = None
    numero_nf: Optional[str] = None
    status: str = ""