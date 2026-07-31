import re


def normalizar_numero_nf(valor: str) -> str | None:
    digitos = re.sub(r"\D", "", valor or "")
    if not digitos:
        return None
    return digitos.lstrip("0") or "0"


def extrair_nf_da_chave(chave: str) -> str | None:
    """Extrai nNF (9 posições) de uma chave NF-e de 44 dígitos."""
    digitos = re.sub(r"\D", "", chave or "")
    if len(digitos) != 44:
        return None
    return normalizar_numero_nf(digitos[25:34])


def extrair_nf_do_texto(texto: str) -> str | None:
    texto = (texto or "").upper().replace("O", "0")
    padroes = (
        r"(?:NF[\s.\-]*E)?[\s\S]{0,20}?N[º°0O#.:;\-]*\s*(\d{5,9})",
        r"\b(0\d{8})\b",
        r"\b(\d{5,9})\b",
    )
    for padrao in padroes:
        achado = re.search(padrao, texto)
        if achado:
            return normalizar_numero_nf(achado.group(1))
    return None
