import re

import numpy as np
import easyocr


_reader = easyocr.Reader(
    ["pt"],
    gpu=False,
    verbose=False
)


def ler_numero_nf(imagem: np.ndarray):
    if imagem is None or imagem.size == 0:
        return None

    resultados = _reader.readtext(
        imagem,
        detail=0,
        paragraph=False,
        decoder="greedy",
        batch_size=1,
        workers=0,
        allowlist=(
            "0123456789"
            "NnFfEe"
            "SsÉéRrIi"
            "º°.- "
        )
    )

    texto = " ".join(resultados).upper()

    print("Texto OCR:", texto)

    padroes = [
        r"NF[\s-]*E?\s*N?\s*[º°O0]?\s*[.:;-]?\s*0*(\d{5,9})",
        r"N\s*[º°O0]?\s*[.:;-]?\s*0*(\d{5,9})",
        r"0*(\d{5,9})\s*S[ÉE]RIE",
        r"0*(\d{5,9})\s*FOLHA",
    ]

    for padrao in padroes:
        resultado = re.search(
            padrao,
            texto,
            flags=re.IGNORECASE
        )

        if resultado:
            return str(int(resultado.group(1)))

    return None