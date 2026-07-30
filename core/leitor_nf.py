import re
from threading import Lock

import cv2
import numpy as np
from rapidocr_onnxruntime import RapidOCR

# O modelo é carregado uma única vez por processo do servidor.
_reader = RapidOCR()
_reader_lock = Lock()

_PADROES = tuple(
    re.compile(padrao, re.IGNORECASE)
    for padrao in (
        r"NF[\s-]*E?\s*N?\s*[º°O0]?\s*[.:;\-]?\s*(\d{5,9})",
        r"N\s*[º°O0]?\s*[.:;\-]?\s*(\d{5,9})",
        r"(\d{5,9})\s*S[ÉE]RIE",
        r"(\d{5,9})\s*FOLHA",
    )
)


def normalizar_texto(texto: str) -> str:
    texto = texto.upper()
    substituicoes = {
        "N°": "Nº",
        "N0": "Nº",
        "NO.": "Nº",
        "NO ": "Nº ",
        "SÉRLE": "SÉRIE",
        "SERIE": "SÉRIE",
    }
    for original, novo in substituicoes.items():
        texto = texto.replace(original, novo)
    return " ".join(texto.split())


def localizar_numero(texto: str) -> str | None:
    texto = normalizar_texto(texto)
    for padrao in _PADROES:
        correspondencia = padrao.search(texto)
        if correspondencia:
            numero = correspondencia.group(1)
            return numero.lstrip("0") or "0"
    return None


def _redimensionar(imagem: np.ndarray, largura_maxima: int = 1100) -> np.ndarray:
    altura, largura = imagem.shape[:2]
    if largura <= largura_maxima:
        return imagem
    proporcao = largura_maxima / largura
    return cv2.resize(
        imagem,
        (largura_maxima, max(1, int(altura * proporcao))),
        interpolation=cv2.INTER_AREA,
    )


def _executar_ocr(imagem: np.ndarray) -> str:
    imagem = _redimensionar(imagem)
    # O objeto RapidOCR não deve executar duas inferências simultâneas.
    with _reader_lock:
        resultado, _ = _reader(imagem)
    if not resultado:
        return ""
    return " ".join(str(item[1]) for item in resultado if len(item) >= 2)


def ler_numero_nf(imagem: np.ndarray) -> str | None:
    if imagem is None or imagem.size == 0:
        return None

    texto = _executar_ocr(imagem)
    numero = localizar_numero(texto)
    if numero:
        return numero

    # Segunda leitura somente quando necessária, com contraste leve.
    if imagem.ndim == 3:
        cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    else:
        cinza = imagem

    tratada = cv2.convertScaleAbs(cinza, alpha=1.25, beta=5)
    return localizar_numero(_executar_ocr(tratada))
