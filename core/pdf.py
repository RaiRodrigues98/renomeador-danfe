"""
Módulo responsável por trabalhar com PDFs.

- Extrai texto pesquisável (PyMuPDF)
- Converte páginas em imagens (PyMuPDF)
"""

from pathlib import Path

import fitz
from PIL import Image

from config import PDF_DPI


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


def extrair_paginas_pdf(pdf_path: Path | str) -> list[Image.Image]:
    """
    Converte todas as páginas do PDF em imagens utilizando PyMuPDF.
    Compatível com Windows, Render e Railway.
    """

    pdf_path = Path(pdf_path).resolve()

    imagens: list[Image.Image] = []

    with fitz.open(pdf_path) as documento:

        for pagina in documento:

            pix = pagina.get_pixmap(
                dpi=PDF_DPI,
                alpha=False
            )

            imagem = Image.frombytes(
                "RGB",
                (pix.width, pix.height),
                pix.samples
            )

            imagens.append(imagem)

    return imagens