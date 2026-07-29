"""
Módulo responsável pela execução do OCR utilizando Tesseract.
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image
from numpy.typing import NDArray

from config import OCR_LANGUAGE, TESSERACT_PATH
from core.image import melhorar_imagem


# Configura o executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = str(TESSERACT_PATH)


Imagem = Image.Image | NDArray[np.uint8]


def ocr_imagem(imagem: Imagem) -> str:
    """
    Executa OCR em uma imagem.

    Aceita:
        - PIL.Image
        - numpy.ndarray (OpenCV)

    Retorna:
        Texto reconhecido pelo Tesseract.
    """

    if isinstance(imagem, Image.Image):
        imagem = cv2.cvtColor(
            np.array(imagem),
            cv2.COLOR_RGB2BGR
        )

    imagem = melhorar_imagem(imagem)

    texto = pytesseract.image_to_string(
        imagem,
        lang=OCR_LANGUAGE,
        config="--oem 3 --psm 6"
    )

    return texto.strip()