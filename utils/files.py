"""
Utilitários para manipulação de arquivos.
"""

from pathlib import Path
from shutil import move


def arquivo_existe(caminho: Path) -> bool:
    """
    Verifica se um arquivo existe.
    """
    return caminho.exists()


def criar_pasta(caminho: Path) -> Path:
    """
    Cria a pasta caso não exista.
    """
    caminho.mkdir(
        parents=True,
        exist_ok=True
    )

    return caminho


def obter_nome_disponivel(caminho: Path) -> Path:
    """
    Retorna um nome disponível caso já exista um arquivo
    com o mesmo nome.

    Exemplo:

    nota.pdf
    nota (1).pdf
    nota (2).pdf
    """

    contador = 1
    destino = caminho

    while destino.exists():

        destino = caminho.with_name(
            f"{caminho.stem} ({contador}){caminho.suffix}"
        )

        contador += 1

    return destino


def renomear_arquivo(
    origem: Path,
    destino: Path
) -> Path:
    """
    Move/renomeia um arquivo evitando sobrescrever outro.
    """

    criar_pasta(destino.parent)

    destino = obter_nome_disponivel(destino)

    move(origem, destino)

    return destino