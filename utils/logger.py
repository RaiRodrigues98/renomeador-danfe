import logging
import sys

from config import LOG_LEVEL


def configurar_logger() -> logging.Logger:
    logger = logging.getLogger("RenomeadorDANFE")
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    )
    logger.addHandler(handler)
    logger.propagate = False
    return logger


logger = configurar_logger()
