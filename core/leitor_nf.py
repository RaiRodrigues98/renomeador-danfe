import re
from functools import lru_cache
from threading import Lock

import cv2
import numpy as np

from config import OCR_MAX_WIDTH

_reader_lock = Lock()

_PADROES_PRIORITARIOS = tuple(
    re.compile(p, re.IGNORECASE)
    for p in (
        r"(?:NF[\s.\-]*E|NOTA\s+FISCAL(?:\s+ELETR[ÔO]NICA)?)\s*(?:N(?:[ÚU]MERO)?\s*)?[Nº°O0#.:;\-]*\s*(\d{1,9})\b",
        r"\bN[º°O0#.:;\-]*\s*(\d{1,9})\s+(?:S[ÉE]RIE|SERIE)\b",
        r"\b(\d{1,9})\s+(?:S[ÉE]RIE|SERIE)\b",
        r"\b(\d{1,9})\s+(?:FOLHA|FL\.?\s*\d)\b",
    )
)


def normalizar_texto(texto: str) -> str:
    texto = (texto or "").upper().replace("\x00", " ")
    texto = texto.replace("SÉRLE", "SÉRIE").replace("SERlE", "SERIE")
    texto = re.sub(r"[\t\r]+", " ", texto)
    texto = re.sub(r" +", " ", texto)
    return texto.strip()


def _numero_valido(valor: str) -> str | None:
    digitos = re.sub(r"\D", "", valor)
    if not digitos or len(digitos) > 9:
        return None
    numero = digitos.lstrip("0") or "0"
    if len(numero) >= 6 and len(set(numero)) == 1:
        return None
    return numero


def localizar_numero(texto: str) -> str | None:
    texto = normalizar_texto(texto)
    for padrao in _PADROES_PRIORITARIOS:
        for correspondencia in padrao.finditer(texto):
            numero = _numero_valido(correspondencia.group(1))
            if numero is not None:
                return numero
    return None


@lru_cache(maxsize=1)
def _obter_reader():
    from rapidocr_onnxruntime import RapidOCR

    return RapidOCR()


def _preparar_imagem(imagem: np.ndarray) -> np.ndarray:
    """Aplica um único tratamento leve antes da única chamada ao OCR."""
    if imagem.ndim == 3:
        imagem = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY)

    altura, largura = imagem.shape[:2]
    if largura > OCR_MAX_WIDTH:
        escala = OCR_MAX_WIDTH / largura
        imagem = cv2.resize(
            imagem,
            (OCR_MAX_WIDTH, max(1, round(altura * escala))),
            interpolation=cv2.INTER_AREA,
        )

    return np.ascontiguousarray(
        cv2.convertScaleAbs(imagem, alpha=1.40, beta=5)
    )


def _executar_ocr(imagem: np.ndarray) -> str:
    with _reader_lock:
        resultado, _ = _obter_reader()(_preparar_imagem(imagem))
    if not resultado:
        return ""
    return "\n".join(
        str(item[1]) for item in resultado if len(item) >= 2 and item[1]
    )


def ler_numero_nf(imagem: np.ndarray) -> str | None:
    """Executa exatamente uma chamada ao OCR no recorte recebido."""
    if imagem is None or imagem.size == 0:
        return None
    return localizar_numero(_executar_ocr(imagem))
