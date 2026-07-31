from pathlib import Path
from typing import Iterator

import fitz
import numpy as np

from config import OCR_CROPS, PDF_DPI


def validar_pdf(pdf_path: Path | str) -> None:
    caminho = Path(pdf_path)
    if not caminho.is_file() or caminho.stat().st_size < 5:
        raise ValueError("Arquivo PDF vazio ou inválido.")
    with caminho.open("rb") as arquivo:
        if arquivo.read(5) != b"%PDF-":
            raise ValueError("O conteúdo enviado não é um PDF válido.")


def extrair_textos_primeira_pagina(pdf_path: Path | str) -> list[str]:
    """Retorna texto linear e texto ordenado por posição da primeira página."""
    with fitz.open(Path(pdf_path)) as documento:
        if documento.page_count == 0:
            raise ValueError("PDF vazio.")
        pagina = documento.load_page(0)
        textos = [pagina.get_text("text", sort=True) or ""]

        blocos = pagina.get_text("blocks", sort=True) or []
        texto_blocos = "\n".join(str(bloco[4]) for bloco in blocos if len(bloco) > 4)
        if texto_blocos and texto_blocos != textos[0]:
            textos.append(texto_blocos)
        return textos


def _pixmap_para_array(pix: fitz.Pixmap) -> np.ndarray:
    imagem = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
        pix.height, pix.width, pix.n
    )
    if pix.n >= 3:
        return np.ascontiguousarray(imagem[:, :, :3])
    return np.ascontiguousarray(imagem)


def renderizar_regioes_ocr(pdf_path: Path | str) -> Iterator[np.ndarray]:
    with fitz.open(Path(pdf_path)) as documento:
        if documento.page_count == 0:
            raise ValueError("PDF vazio.")

        pagina = documento.load_page(0)
        area = pagina.rect
        for x1, y1, x2, y2 in OCR_CROPS:
            clip = fitz.Rect(
                area.x0 + area.width * x1,
                area.y0 + area.height * y1,
                area.x0 + area.width * x2,
                area.y0 + area.height * y2,
            )
            pix = pagina.get_pixmap(dpi=PDF_DPI, alpha=False, clip=clip)
            yield _pixmap_para_array(pix)
