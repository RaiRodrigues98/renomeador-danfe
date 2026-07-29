"""
Extração inteligente da NF utilizando RapidOCR.
"""

import re
from typing import Optional

from rapidocr_onnxruntime import RapidOCR

from core.image import melhorar_imagem


reader = RapidOCR()


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
    reconhecidas pelo RapidOCR.
    """

    imagem = melhorar_imagem(imagem)

    resultados, _ = reader(imagem)

    if not resultados:
        return None

    palavras = []

    for bbox, texto, confianca in resultados:

        texto = texto.strip().upper()

        if not texto:
            continue

        if confianca < 0.40:
            continue

        x = int(min(p[0] for p in bbox))
        y = int(min(p[1] for p in bbox))
        w = int(max(p[0] for p in bbox) - x)
        h = int(max(p[1] for p in bbox) - y)

        palavras.append(
            {
                "texto": texto.replace(".", ""),
                "x": x,
                "y": y,
                "w": w,
                "h": h,
            }
        )

    palavras.sort(key=lambda p: (p["y"], p["x"]))

    for indice, palavra in enumerate(palavras):

        if palavra["texto"] not in PALAVRAS_CHAVE:
            continue

        for proxima in palavras[indice:indice + 8]:

            numero = re.sub(r"\D", "", proxima["texto"])

            if 5 <= len(numero) <= 9:
                return numero.lstrip("0") or "0"

    return None