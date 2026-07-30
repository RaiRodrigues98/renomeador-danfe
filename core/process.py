from pathlib import Path

from core.leitor_nf import ler_numero_nf, localizar_numero
from core.models import ResultadoProcessamento
from core.pdf import extrair_texto_primeira_pagina, renderizar_recorte_nf
from utils.files import mover_arquivo
from utils.logger import logger


def processar_pdf(pdf_path: Path, pasta_saida: Path) -> ResultadoProcessamento:
    logger.info("Processando: %s", pdf_path.name)

    try:
        # PDFs digitais são resolvidos sem OCR, o que reduz bastante o tempo.
        texto_pdf = extrair_texto_primeira_pagina(pdf_path)
        numero = localizar_numero(texto_pdf)

        # OCR é usado apenas em PDFs digitalizados ou sem texto útil.
        if numero is None:
            recorte = renderizar_recorte_nf(pdf_path)
            numero = ler_numero_nf(recorte)

        if numero is None:
            return ResultadoProcessamento(
                arquivo_original=pdf_path.name,
                status="NF não localizada",
            )

        destino = mover_arquivo(pdf_path, pasta_saida / f"{numero}.pdf")
        return ResultadoProcessamento(
            arquivo_original=pdf_path.name,
            arquivo_final=destino.name,
            numero_nf=numero,
            status="Sucesso",
        )

    except Exception as erro:
        logger.exception("Erro ao processar %s", pdf_path.name)
        return ResultadoProcessamento(
            arquivo_original=pdf_path.name,
            status=f"Erro: {erro}",
        )
