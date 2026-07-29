"""
Módulo responsável pela execução do OCR utilizando RapidOCR.
"""

import cv2
import numpy as np
from PIL import Image
from numpy.typing import NDArray
from rapidocr_onnxruntime import RapidOCR

from core.image import melhorar_imagem


# Inicializa o OCR apenas uma vez
reader = RapidOCR()


Imagem = Image.Image | NDArray[np.uint8]


def ocr_imagem(imagem: Imagem) -> str:
    """
    Executa OCR utilizando RapidOCR.

    Aceita:
        - PIL.Image
        - numpy.ndarray

    Retorna:
        Texto reconhecido.
    """

    if isinstance(imagem, Image.Image):
        imagem = cv2.cvtColor(
            np.array(imagem),
            cv2.COLOR_RGB2BGR
        )

    imagem = melhorar_imagem(imagem)

    resultado, _ = reader(imagem)

    if not resultado:
        return ""

    textos = []

    for item in resultado:
        textos.append(item[1])

    return " ".join(textos).strip()