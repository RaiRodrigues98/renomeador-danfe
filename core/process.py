from pathlib import Path
from time import perf_counter

from config import BARCODE_CROP, BARCODE_DPI, OCR_CROP, OCR_DPI
from core.barcode import ler_nf_codigo_barras
from core.models import ResultadoProcessamento
from core.ocr import ler_nf_ocr
from core.pdf import renderizar_recorte, validar_pdf
from utils.files import mover_arquivo
from utils.logger import logger


def processar_pdf(pdf_path: Path, pasta_saida: Path) -> ResultadoProcessamento:
    inicio = perf_counter()
    logger.info("Processando arquivo=%s", pdf_path.name)
    try:
        validar_pdf(pdf_path)

        inicio_barcode = perf_counter()
        imagem_barcode = renderizar_recorte(pdf_path, BARCODE_CROP, BARCODE_DPI)
        numero, chave = ler_nf_codigo_barras(imagem_barcode)
        tempo_barcode = perf_counter() - inicio_barcode
        metodo = "codigo-barras"

        if numero is None:
            inicio_ocr = perf_counter()
            imagem_ocr = renderizar_recorte(pdf_path, OCR_CROP, OCR_DPI)
            numero, texto_ocr = ler_nf_ocr(imagem_ocr)
            tempo_ocr = perf_counter() - inicio_ocr
            metodo = "ocr-fallback"
            logger.info(
                "Fallback OCR arquivo=%s tempo=%.3fs texto=%r",
                pdf_path.name,
                tempo_ocr,
                texto_ocr[:100],
            )

        if numero is None:
            logger.warning(
                "NF não localizada arquivo=%s barcode_tempo=%.3fs",
                pdf_path.name,
                tempo_barcode,
            )
            return ResultadoProcessamento(
                arquivo_original=pdf_path.name,
                status="NF não localizada",
            )

        destino = mover_arquivo(pdf_path, pasta_saida / f"{numero}.pdf")
        total = perf_counter() - inicio
        logger.info(
            "Arquivo processado arquivo=%s nf=%s metodo=%s chave=%s tempo=%.3fs destino=%s",
            pdf_path.name,
            numero,
            metodo,
            chave or "-",
            total,
            destino.name,
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
