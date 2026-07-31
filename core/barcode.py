from PIL import Image, ImageEnhance, ImageOps
from pyzbar.pyzbar import ZBarSymbol, decode

from core.extractor import extrair_nf_da_chave


def ler_nf_codigo_barras(imagem: Image.Image) -> tuple[str | None, str | None]:
    """Retorna (numero_nf, chave). Faz duas leituras leves no mesmo recorte."""
    variantes = (
        imagem.convert("L"),
        ImageEnhance.Contrast(ImageOps.autocontrast(imagem.convert("L"))).enhance(1.4),
    )
    for variante in variantes:
        resultados = decode(variante, symbols=[ZBarSymbol.CODE128])
        for resultado in resultados:
            chave = resultado.data.decode("ascii", errors="ignore")
            numero = extrair_nf_da_chave(chave)
            if numero:
                return numero, chave
    return None, None
