import re

import cv2
import numpy as np
from rapidocr_onnxruntime import RapidOCR


_reader = RapidOCR()


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


def redimensionar_para_ocr(
    imagem: np.ndarray,
    largura_maxima: int = 1200
) -> np.ndarray:
    """
    Reduz imagens grandes para evitar processamento excessivo.
    Não aumenta imagens pequenas.
    """

    altura, largura = imagem.shape[:2]

    if largura <= largura_maxima:
        return imagem

    proporcao = largura_maxima / largura

    nova_altura = max(
        1,
        int(altura * proporcao)
    )

    return cv2.resize(
        imagem,
        (largura_maxima, nova_altura),
        interpolation=cv2.INTER_AREA
    )


def extrair_texto(imagem: np.ndarray) -> str:
    resultado, _ = _reader(imagem)

    if not resultado:
        return ""

    textos = [
        str(item[1])
        for item in resultado
        if len(item) >= 2
    ]

    return normalizar_texto(
        " ".join(textos)
    )


def localizar_numero(texto: str) -> str | None:
    padroes = [
        r"NF[\s-]*E?\s*N?\s*[º°O0]?\s*[.:;-]?\s*(\d{5,9})",
        r"N\s*[º°O0]?\s*[.:;-]?\s*(\d{5,9})",
        r"(\d{5,9})\s*S[ÉE]RIE",
        r"(\d{5,9})\s*FOLHA",
    ]

    for padrao in padroes:
        correspondencia = re.search(
            padrao,
            texto,
            flags=re.IGNORECASE
        )

        if correspondencia:
            numero = correspondencia.group(1)

            return numero.lstrip("0") or "0"

    return None


def procurar_numero(imagem: np.ndarray) -> str | None:
    imagem = redimensionar_para_ocr(imagem)

    texto = extrair_texto(imagem)

    print(f"Texto OCR: {texto[:500]}")

    if not texto:
        return None

    return localizar_numero(texto)


def ler_numero_nf(imagem: np.ndarray) -> str | None:
    if imagem is None or imagem.size == 0:
        return None

    # Primeira tentativa
    numero = procurar_numero(imagem)

    if numero:
        print(f"NF encontrada: {numero}")
        return numero

    # Segunda tentativa sem ampliar a imagem
    if len(imagem.shape) == 3:
        cinza = cv2.cvtColor(
            imagem,
            cv2.COLOR_BGR2GRAY
        )
    else:
        cinza = imagem

    numero = procurar_numero(cinza)

    if numero:
        print(
            f"NF encontrada após conversão para cinza: {numero}"
        )

    return numero