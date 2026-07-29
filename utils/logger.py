"""
Configuração centralizada de logs do projeto.
"""

import logging
from pathlib import Path

from config import LOG_DIR

# Cria a pasta de logs caso não exista
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "renomeador.log"


def configurar_logger() -> logging.Logger:
    """
    Configura e retorna o logger principal do projeto.
    """

    logger = logging.getLogger("RenomeadorNF")

    # Evita adicionar handlers duplicados
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        "%d/%m/%Y %H:%M:%S"
    )

    # Salva no arquivo
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    # Exibe no terminal
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = configurar_logger()