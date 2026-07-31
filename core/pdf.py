from pathlib import Path

import fitz
from PIL import Image


def validar_pdf(pdf_path: Path | str) -> None:
    caminho = Path(pdf_path)
    if not caminho.is_file() or caminho.stat().st_size < 5:
        raise ValueError("Arquivo PDF vazio ou inválido.")
    with caminho.open("rb") as arquivo:
        if arquivo.read(5) != b"%PDF-":
            raise ValueError("O conteúdo enviado não é um PDF válido.")


def renderizar_recorte(
    pdf_path: Path | str,
    crop: tuple[float, float, float, float],
    dpi: int,
) -> Image.Image:
    with fitz.open(Path(pdf_path)) as documento:
        if documento.page_count == 0:
            raise ValueError("PDF vazio.")
        pagina = documento.load_page(0)
        area = pagina.rect
        x1, y1, x2, y2 = crop
        clip = fitz.Rect(
            area.x0 + area.width * x1,
            area.y0 + area.height * y1,
            area.x0 + area.width * x2,
            area.y0 + area.height * y2,
        )
        pix = pagina.get_pixmap(dpi=dpi, alpha=False, clip=clip)
        modo = "RGB" if pix.n >= 3 else "L"
        return Image.frombytes(modo, (pix.width, pix.height), pix.samples)
