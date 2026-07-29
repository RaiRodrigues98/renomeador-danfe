import cv2
import numpy as np

from config import (
    CROP_X1,
    CROP_Y1,
    CROP_X2,
    CROP_Y2,
)


def recortar_numero_nota(imagem: np.ndarray) -> np.ndarray:
    altura, largura = imagem.shape[:2]

    x1 = int(largura * CROP_X1)
    y1 = int(altura * CROP_Y1)
    x2 = int(largura * CROP_X2)
    y2 = int(altura * CROP_Y2)

    return imagem[y1:y2, x1:x2]


def melhorar_imagem(imagem: np.ndarray) -> np.ndarray:

    cinza = cv2.cvtColor(
        imagem,
        cv2.COLOR_BGR2GRAY
    )

    # Aumenta um pouco o contraste
    cinza = cv2.convertScaleAbs(
        cinza,
        alpha=1.4,
        beta=10
    )

    # Amplia antes do OCR
    ampliada = cv2.resize(
        cinza,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    return ampliada