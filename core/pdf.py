from pathlib import Path

import cv2
import fitz
import numpy as np

from config import CROP_X1, CROP_X2, CROP_Y1, CROP_Y2, PDF_DPI


def extrair_texto_primeira_pagina(pdf_path: Path | str) -> str:
    with fitz.open(Path(pdf_path)) as documento:
        if documento.page_count == 0:
            raise ValueError("PDF vazio.")
        return documento.load_page(0).get_text("text") or ""


def renderizar_recorte_nf(pdf_path: Path | str) -> np.ndarray:
    """Renderiza somente a região onde normalmente aparece o número da NF."""
    with fitz.open(Path(pdf_path)) as documento:
        if documento.page_count == 0:
            raise ValueError("PDF vazio.")

        pagina = documento.load_page(0)
        retangulo = pagina.rect
        clip = fitz.Rect(
            retangulo.x0 + retangulo.width * CROP_X1,
            retangulo.y0 + retangulo.height * CROP_Y1,
            retangulo.x0 + retangulo.width * CROP_X2,
            retangulo.y0 + retangulo.height * CROP_Y2,
        )
        pix = pagina.get_pixmap(dpi=PDF_DPI, alpha=False, clip=clip)
        imagem = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
            pix.height, pix.width, pix.n
        )
        if pix.n == 4:
            return cv2.cvtColor(imagem, cv2.COLOR_RGBA2BGR)
        return cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR)
