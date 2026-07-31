import cv2
import numpy as np


def recortar_numero_nota(
    imagem: np.ndarray,
) -> np.ndarray:
    """
    Recorta apenas a região onde normalmente está o número da DANFE.
    """

    altura, largura = imagem.shape[:2]

    return imagem[
        int(altura * 0.00):int(altura * 0.18),
        int(largura * 0.60):int(largura * 1.00),
    ]


def melhorar_imagem(
    imagem: np.ndarray,
) -> np.ndarray:
    """
    Melhora somente quando o OCR for necessário.
    """

    if len(imagem.shape) == 3:

        imagem = cv2.cvtColor(
            imagem,
            cv2.COLOR_BGR2GRAY
        )

    # Redução de ruído
    imagem = cv2.GaussianBlur(
        imagem,
        (3, 3),
        0
    )

    # Binarização adaptativa
    imagem = cv2.adaptiveThreshold(
        imagem,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        8
    )

    return imagem


def reduzir_para_ocr(
    imagem: np.ndarray,
    largura_maxima: int = 1200,
) -> np.ndarray:
    """
    Evita enviar imagens enormes ao OCR.
    """

    altura, largura = imagem.shape[:2]

    if largura <= largura_maxima:
        return imagem

    proporcao = largura_maxima / largura

    nova_altura = int(
        altura * proporcao
    )

    return cv2.resize(
        imagem,
        (largura_maxima, nova_altura),
        interpolation=cv2.INTER_AREA
    )