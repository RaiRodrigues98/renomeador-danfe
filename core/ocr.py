"""
Módulo responsável pela execução do OCR utilizando EasyOCR.
"""

import numpy as np
import cv2
import easyocr
from PIL import Image
from numpy.typing import NDArray

from core.image import melhorar_imagem

# Cria o leitor apenas uma vez
reader = easyocr.Reader(
    ['pt'],
    gpu=False
)

Imagem = Image.Image | NDArray[np.uint8]


def ocr_imagem(imagem: Imagem) -> str:
    """
    Executa OCR utilizando EasyOCR.

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

    resultado = reader.readtext(
        imagem,
        detail=0,
        paragraph=True
    )

    return " ".join(resultado).strip()