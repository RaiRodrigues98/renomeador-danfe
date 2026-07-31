import re
from functools import lru_cache
from threading import Lock

import cv2
import numpy as np

from config import OCR_MAX_WIDTH

_reader_lock = Lock()

# O rótulo é obrigatório para reduzir falsos positivos com CNPJ, chave e série.
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
    # Rejeita sequências claramente improváveis produzidas pelo OCR.
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
    # Inicialização preguiçosa: o healthcheck responde sem aguardar o modelo OCR.
    from rapidocr_onnxruntime import RapidOCR

    return RapidOCR()


def _redimensionar(imagem: np.ndarray) -> np.ndarray:
    altura, largura = imagem.shape[:2]
    if largura <= OCR_MAX_WIDTH:
        return imagem
    escala = OCR_MAX_WIDTH / largura
    return cv2.resize(
        imagem,
        (OCR_MAX_WIDTH, max(1, round(altura * escala))),
        interpolation=cv2.INTER_AREA,
    )


def _executar_ocr(imagem: np.ndarray) -> str:
    imagem = _redimensionar(np.ascontiguousarray(imagem))
    with _reader_lock:
        resultado, _ = _obter_reader()(imagem)
    if not resultado:
        return ""
    linhas = [str(item[1]) for item in resultado if len(item) >= 2 and item[1]]
    return "\n".join(linhas)


def _variacoes(imagem: np.ndarray):
    yield imagem
    cinza = cv2.cvtColor(imagem, cv2.COLOR_RGB2GRAY) if imagem.ndim == 3 else imagem
    yield cv2.convertScaleAbs(cinza, alpha=1.35, beta=8)
    yield cv2.threshold(cinza, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def ler_numero_nf(imagem: np.ndarray) -> str | None:
    if imagem is None or imagem.size == 0:
        return None
    for variacao in _variacoes(imagem):
        numero = localizar_numero(_executar_ocr(variacao))
        if numero:
            return numero
    return None
