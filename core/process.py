from pathlib import Path
from time import perf_counter

from core.leitor_nf import ler_numero_nf, localizar_numero
from core.models import ResultadoProcessamento
from core.pdf import extrair_textos_primeira_pagina, renderizar_regioes_ocr, validar_pdf
from utils.files import mover_arquivo
from utils.logger import logger


def processar_pdf(pdf_path: Path, pasta_saida: Path) -> ResultadoProcessamento:
    inicio = perf_counter()
    logger.info("Processando arquivo=%s", pdf_path.name)
    try:
        validar_pdf(pdf_path)

        numero = None
        metodo = "texto"
        for texto in extrair_textos_primeira_pagina(pdf_path):
            numero = localizar_numero(texto)
            if numero:
                break

        if numero is None:
            metodo = "ocr"
            for imagem in renderizar_regioes_ocr(pdf_path):
                numero = ler_numero_nf(imagem)
                if numero:
                    break

        if numero is None:
            logger.warning("NF não localizada arquivo=%s", pdf_path.name)
            return ResultadoProcessamento(
                arquivo_original=pdf_path.name,
                status="NF não localizada",
            )

        destino = mover_arquivo(pdf_path, pasta_saida / f"{numero}.pdf")
        logger.info(
            "Arquivo processado arquivo=%s nf=%s metodo=%s destino=%s",
            pdf_path.name,
            numero,
            metodo,
            destino.name,
        )
        logger.info(
            "Tempo de processamento arquivo=%s segundos=%.2f",
            pdf_path.name,
            perf_counter() - inicio,
        )
        return ResultadoProcessamento(
            arquivo_original=pdf_path.name,
            arquivo_final=destino.name,
            numero_nf=numero,
            status="Sucesso",
        )
    except Exception as erro:
        logger.exception("Falha ao processar arquivo=%s", pdf_path.name)
        return ResultadoProcessamento(
            arquivo_original=pdf_path.name,
            status=f"Erro: {erro}",
        )
