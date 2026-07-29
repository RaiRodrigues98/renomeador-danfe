"""
Extração do número da NF-e.
"""

import re
from typing import Optional


SUBSTITUICOES = {
    "NO.": "Nº",
    "NO ": "Nº ",
    "N°": "Nº",
    "N.": "Nº",
    "N?": "Nº",
    "N O": "Nº",
    "Nº.": "Nº",
}

PADROES = [
    re.compile(
        r"NF[\s\-]?E.{0,50}?N[º]?\s*[:.]?\s*(0*\d{5,9})",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"DANFE.{0,80}?N[º]?\s*[:.]?\s*(0*\d{5,9})",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"N[ÚU]MERO\s*[:.]?\s*(0*\d{5,9})",
        re.IGNORECASE,
    ),
    re.compile(
        r"N[º]?\s*[:.]?\s*(0*\d{5,9})",
        re.IGNORECASE,
    ),
]


def normalizar_texto(texto: str) -> str:

    texto = texto.upper()

    for antigo, novo in SUBSTITUICOES.items():
        texto = texto.replace(antigo, novo)

    return re.sub(r"\s+", " ", texto)


def limpar_numero(numero: str) -> str:
    numero = re.sub(r"\D", "", numero)
    return numero.lstrip("0") or "0"


def localizar_numero_nf(texto: str) -> Optional[str]:

    if not texto:
        return None

    texto = normalizar_texto(texto)

    encontrados = []

    for padrao in PADROES:

        for match in padrao.finditer(texto):

            numero = limpar_numero(match.group(1))

            if 5 <= len(numero) <= 9:
                encontrados.append(numero)

    if not encontrados:

        for numero in re.findall(r"\b0*\d{5,9}\b", texto):

            numero = limpar_numero(numero)

            if 5 <= len(numero) <= 9:
                encontrados.append(numero)

    if not encontrados:
        return None

    return next(iter(dict.fromkeys(encontrados)))