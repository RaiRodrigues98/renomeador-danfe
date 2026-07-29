"""
Módulo responsável por converter a primeira página do PDF em imagem OpenCV.
"""

from pathlib import Path

import cv2
import fitz
import numpy as np

from config import PDF_DPI


def pdf_para_imagem(pdf_path: Path |str) -> np.ndarray:

    pdf_path = Path(pdf_path).resolve()

    with fitz.open(pdf_path) as documento:

        if documento.page_count == 0:
            raise ValueError("PDF vazio.")

        pagina = documento.load_page(0)

        pix = pagina.get_pixmap(
            dpi=PDF_DPI,
            alpha=False
        )

        imagem = np.frombuffer(
            pix.samples,
            dtype=np.uint8
        ).reshape(
            pix.height,
            pix.width,
            pix.n
        )

        return cv2.cvtColor(
            imagem,
            cv2.COLOR_RGB2BGR
        )