import re
import shutil
import time
from pathlib import Path

from config import SESSION_TTL_HOURS, SESSIONS_DIR

_CARACTERES_INVALIDOS = re.compile(r"[^A-Za-z0-9._() \-]+")


def nome_seguro(nome: str) -> str:
    nome = Path(nome).name.strip()
    nome = _CARACTERES_INVALIDOS.sub("_", nome)
    return nome[:180] or "arquivo.pdf"


def obter_nome_disponivel(caminho: Path) -> Path:
    if not caminho.exists():
        return caminho
    contador = 1
    while True:
        candidato = caminho.with_name(
            f"{caminho.stem} ({contador}){caminho.suffix}"
        )
        if not candidato.exists():
            return candidato
        contador += 1


def mover_arquivo(origem: Path, destino: Path) -> Path:
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino = obter_nome_disponivel(destino)
    return Path(shutil.move(str(origem), str(destino)))


def pasta_sessao(sessao_id: str) -> Path:
    if not re.fullmatch(r"[a-f0-9]{32}", sessao_id):
        raise ValueError("Identificador de sessão inválido.")
    return SESSIONS_DIR / sessao_id


def limpar_sessoes_antigas() -> None:
    limite = time.time() - (SESSION_TTL_HOURS * 3600)
    if not SESSIONS_DIR.exists():
        return
    for pasta in SESSIONS_DIR.iterdir():
        try:
            if pasta.is_dir() and pasta.stat().st_mtime < limite:
                shutil.rmtree(pasta, ignore_errors=True)
        except OSError:
            continue
