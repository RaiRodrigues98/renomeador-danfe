import cv2
import numpy as np
from PIL import Image
from numpy.typing import NDArray


Imagem = Image.Image | NDArray[np.uint8]


def recortar_numero_nota(imagem: Imagem) -> Imagem:
    """
    Recorta a região onde normalmente fica o número da NF.
    """

    if isinstance(imagem, Image.Image):
        largura, altura = imagem.size
        return imagem.crop((
            int(largura * 0.58),
            int(altura * 0.02),
            int(largura * 0.98),
            int(altura * 0.28)
        ))

    altura, largura = imagem.shape[:2]

    return imagem[
        int(altura * 0.02):int(altura * 0.28),
        int(largura * 0.58):int(largura * 0.98)
    ]


def recortar_topo_pagina(imagem: Imagem) -> Imagem:
    """
    Recorta aproximadamente o terço superior da página.
    """

    if isinstance(imagem, Image.Image):
        largura, altura = imagem.size
        return imagem.crop((0, 0, largura, int(altura * 0.35)))

    altura, largura = imagem.shape[:2]

    return imagem[
        0:int(altura * 0.35),
        0:largura
    ]


def melhorar_imagem(imagem: Imagem) -> NDArray[np.uint8]:
    """
    Pré-processa a imagem para OCR.
    """

    if isinstance(imagem, Image.Image):
        imagem = np.array(imagem)
        imagem = cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR)

    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    borrada = cv2.GaussianBlur(
        cinza,
        (3, 3),
        0
    )

    _, binaria = cv2.threshold(
        borrada,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    ampliada = cv2.resize(
        binaria,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    kernel = np.array(
        [
            [-1, -1, -1],
            [-1,  9, -1],
            [-1, -1, -1]
        ],
        dtype=np.int8
    )

    return cv2.filter2D(
        ampliada,
        -1,
        kernel
    )