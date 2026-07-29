"""
Extração inteligente da NF utilizando OCR com coordenadas.
"""

import re
from typing import Optional

import pytesseract

from config import OCR_LANGUAGE
from core.image import melhorar_imagem


PALAVRAS_CHAVE = {
    "NF",
    "NF-E",
    "NFE",
    "DANFE",
    "Nº",
    "NO",
    "NUMERO",
    "NÚMERO",
}


def extrair_nf_por_coordenadas(imagem) -> Optional[str]:
    """
    Localiza o número da NF analisando a posição das palavras
    reconhecidas pelo OCR.
    """

    imagem = melhorar_imagem(imagem)

    dados = pytesseract.image_to_data(
        imagem,
        lang=OCR_LANGUAGE,
        config="--oem 3 --psm 7",
        output_type=pytesseract.Output.DICT,
    )

    palavras = []

    for i, texto in enumerate(dados["text"]):

        texto = texto.strip().upper()

        if not texto:
            continue

        try:
            confianca = float(dados["conf"][i])
        except ValueError:
            confianca = -1

        if confianca < 40:
            continue

        palavras.append(
            {
                "texto": texto.replace(".", ""),
                "x": dados["left"][i],
                "y": dados["top"][i],
                "w": dados["width"][i],
                "h": dados["height"][i],
            }
        )

    for indice, palavra in enumerate(palavras):

        if palavra["texto"] not in PALAVRAS_CHAVE:
            continue

        for proxima in palavras[indice:indice + 8]:

            numero = re.sub(r"\D", "", proxima["texto"])

            if 5 <= len(numero) <= 9:
                return numero.lstrip("0") or "0"

    return None