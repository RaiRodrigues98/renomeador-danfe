import re

import numpy as np

try:
    import easyocr

    _reader = easyocr.Reader(
        ["pt"],
        gpu=False,
        verbose=False
    )
except Exception:
    _reader = None


def procurar_numero(imagem):

    resultados = _reader.readtext(
        imagem,
        detail=0,
        paragraph=True
    )

    texto = " ".join(resultados)

    print("\n========================")
    print(texto)
    print("========================")

    padroes = [

        # Nº 000046951
        r"N[º°o]?\s*\.?\s*0*(\d{5,9})",

        # No. 000046951
        r"No\.?\s*0*(\d{5,9})",

        # 000046951 SÉRIE
        r"0*(\d{5,9})\s*S[ÉE]RIE",

        # 000046951 FOLHA
        r"0*(\d{5,9})\s*FOLHA",
    ]

    for padrao in padroes:

        m = re.search(
            padrao,
            texto,
            flags=re.IGNORECASE
        )

        if m:
            return str(int(m.group(1)))

    return None


def ler_numero_nf(imagem: np.ndarray):

    if _reader is None:
        return None

    altura, largura = imagem.shape[:2]

    regioes = [

        # 1 - Campo NF-e (superior direita)
        imagem[
            0:int(altura * 0.28),
            int(largura * 0.72):largura
        ],

        # 2 - Bloco DANFE
        imagem[
            int(altura * 0.12):int(altura * 0.55),
            int(largura * 0.22):int(largura * 0.60)
        ],

        # 3 - Parte superior inteira
        imagem[
            0:int(altura * 0.40),
            :
        ],

        # 4 - Documento inteiro
        imagem
    ]

    for indice, regiao in enumerate(regioes):

        print(f"\nTentativa {indice + 1}")

        numero = procurar_numero(regiao)

        if numero:
            print(f"NF encontrada: {numero}")
            return numero

    return None