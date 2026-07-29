"""
Utilitários para manipulação de arquivos.
"""

from pathlib import Path
from shutil import move


def criar_pasta(caminho: Path) -> Path:
    caminho.mkdir(
        parents=True,
        exist_ok=True
    )
    return caminho


def obter_nome_disponivel(caminho: Path) -> Path:

    if not caminho.exists():
        return caminho

    contador = 1

    while True:

        novo = caminho.with_name(
            f"{caminho.stem} ({contador}){caminho.suffix}"
        )

        if not novo.exists():
            return novo

        contador += 1


def renomear_arquivo(
    origem: Path,
    destino: Path
) -> Path:

    criar_pasta(destino.parent)

    destino = obter_nome_disponivel(destino)

    move(
        str(origem),
        str(destino)
    )

    return destino