from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import pytesseract

from core.extractor import extrair_nf_do_texto


def ler_nf_ocr(imagem: Image.Image) -> tuple[str | None, str]:
    cinza = ImageOps.grayscale(imagem)
    cinza = ImageOps.autocontrast(cinza)
    cinza = ImageEnhance.Contrast(cinza).enhance(1.6)
    cinza = cinza.resize((cinza.width * 2, cinza.height * 2))
    cinza = cinza.filter(ImageFilter.SHARPEN)
    texto = pytesseract.image_to_string(
        cinza,
        config="--oem 1 --psm 6 -c tessedit_char_whitelist=0123456789NnOo.-",
    )
    return extrair_nf_do_texto(texto), texto.strip()
