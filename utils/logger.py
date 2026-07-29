"""
Configuração centralizada de logs do projeto.
"""

import logging

from config import LOG_DIR


LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)

LOG_FILE = LOG_DIR / "renomeador.log"


def configurar_logger() -> logging.Logger:
    """
    Configura o logger principal do projeto.
    """

    logger = logging.getLogger("RenomeadorDANFE")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        "%d/%m/%Y %H:%M:%S"
    )

    arquivo = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    arquivo.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    logger.addHandler(arquivo)
    logger.addHandler(console)

    logger.propagate = False

    return logger


logger = configurar_logger()