"""
Módulo responsável por trabalhar com PDFs.

- Extrai texto pesquisável (PyMuPDF)
- Converte páginas em imagens (pdf2image)
"""

from pathlib import Path

import fitz
from PIL import Image
from pdf2image import convert_from_path

from config import PDF_DPI, POPPLER_PATH


def extrair_texto_pdf(pdf_path: Path | str) -> str:
    """
    Extrai o texto da primeira página do PDF.

    Retorna uma string vazia caso o PDF não possua texto.
    """

    pdf_path = Path(pdf_path).resolve()

    try:

        with fitz.open(pdf_path) as documento:

            if documento.page_count == 0:
                return ""

            return documento[0].get_text("text").strip()

    except Exception:

        return ""


def extrair_paginas_pdf(
    pdf_path: Path | str
) -> list[Image.Image]:
    """
    Converte o PDF em imagens.
    """

    pdf_path = Path(pdf_path).resolve()

    return convert_from_path(
        pdf_path=str(pdf_path),
        dpi=PDF_DPI,
        poppler_path=str(POPPLER_PATH)
    )