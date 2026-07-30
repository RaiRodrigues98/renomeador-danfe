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
        "SÉRlE": "SÉRIE",
    }

    for antigo, novo in substituicoes.items():
        texto = texto.replace(antigo, novo)

    return " ".join(texto.split())


def procurar_numero(imagem: np.ndarray):
    resultado, _ = _reader(imagem)

    if not resultado:
        print("RapidOCR não reconheceu nenhum texto.")
        return None

    textos = []

    for item in resultado:
        if len(item) >= 2:
            textos.append(str(item[1]))

    texto = normalizar_texto(" ".join(textos))

    print("\n========================")
    print("TEXTO RECONHECIDO:")
    print(texto)
    print("========================")

    padroes = [
        # Nº 000047375
        r"N\s*[º°O0]?\s*[.:;-]?\s*(\d{5,9})",

        # NF-e Nº 000047375
        r"NF[\s-]*E?\s*N?\s*[º°O0]?\s*[.:;-]?\s*(\d{5,9})",

        # 000047375 SÉRIE
        r"(\d{5,9})\s*S[ÉE]RIE",

        # 000047375 FOLHA
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

            # Remove zeros iniciais:
            return numero.lstrip("0") or "0"

    return None


def ler_numero_nf(imagem: np.ndarray):
    if imagem is None or imagem.size == 0:
        print("Imagem vazia recebida pelo OCR.")
        return None

    tentativas = [imagem]

    # Converte para escala de cinza
    if len(imagem.shape) == 3:
        cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    else:
        cinza = imagem

    # Ampliação
    ampliada = cv2.resize(
        cinza,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    tentativas.append(ampliada)

    # Binarização
    binaria = cv2.adaptiveThreshold(
        ampliada,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        10
    )

    tentativas.append(binaria)

    for indice, tentativa in enumerate(tentativas, start=1):
        print(f"Tentativa OCR {indice}")

        numero = procurar_numero(tentativa)

        if numero:
            print(f"NF encontrada: {numero}")
            return numero

    print("Número da NF não encontrado.")
    return None