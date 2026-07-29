from pathlib import Path
from typing import Callable
from core.extractor import extrair_nf_por_coordenadas
from core.image import (
    recortar_numero_nota,
    recortar_topo_pagina
)
from core.models import ResultadoProcessamento
from core.ocr import ocr_imagem
from core.pdf import (
    extrair_paginas_pdf,
    extrair_texto_pdf
)
from core.regex import localizar_numero_nf
from core.statistics import Estatisticas

from utils.files import renomear_arquivo
from utils.logger import logger


def processar_pdf(
    pdf_path: Path,
    pasta_saida: Path | None = None
) -> ResultadoProcessamento:
    """
    Processa um único PDF.
    """

    logger.info(f"Processando: {pdf_path.name}")

    try:

        # ===========================================================
        # 1ª tentativa - Texto pesquisável (PyMuPDF)
        # ===========================================================

        texto = extrair_texto_pdf(pdf_path)
        numero = localizar_numero_nf(texto)

        # ===========================================================
        # 2ª tentativa - OCR
        # ===========================================================

        if numero is None:

            paginas = extrair_paginas_pdf(pdf_path)

            if not paginas:
                return ResultadoProcessamento(
                    arquivo_original=pdf_path.name,
                    arquivo_final=None,
                    numero_nf=None,
                    status="Erro ao abrir PDF"
                )

            pagina = paginas[0]

            # =======================================================
            # Recorte da caixa da NF
            # =======================================================

            recorte = recortar_numero_nota(pagina)

            numero = extrair_nf_por_coordenadas(recorte)

            if numero is None:

                texto = ocr_imagem(recorte)
                numero = localizar_numero_nf(texto)

            # =======================================================
            # Metade superior da página
            # =======================================================

            if numero is None:

                topo = recortar_topo_pagina(pagina)

                numero = extrair_nf_por_coordenadas(topo)

                if numero is None:

                    texto = ocr_imagem(topo)
                    numero = localizar_numero_nf(texto)

        # ===========================================================
        # Resultado
        # ===========================================================

        if numero is None:

            logger.warning(f"NF não localizada: {pdf_path.name}")

            return ResultadoProcessamento(
                arquivo_original=pdf_path.name,
                arquivo_final=None,
                numero_nf=None,
                status="NF não localizada"
            )

        novo_nome = f"{numero}.pdf"

        if pasta_saida:
            pasta_saida.mkdir(parents=True, exist_ok=True)
            novo_caminho = pasta_saida / novo_nome
        else:
            novo_caminho = pdf_path.with_name(novo_nome)

        novo_caminho = renomear_arquivo(
            pdf_path,
            novo_caminho
        )

        logger.info(
            f"{pdf_path.name} -> {novo_caminho.name}"
        )

        return ResultadoProcessamento(
            arquivo_original=pdf_path.name,
            arquivo_final=novo_caminho.name,
            numero_nf=numero,
            status="Sucesso"
        )

    except Exception as e:

        logger.exception(e)

        return ResultadoProcessamento(
            arquivo_original=pdf_path.name,
            arquivo_final=None,
            numero_nf=None,
            status=f"Erro: {e}"
        )


def processar_pasta(
    pasta: Path,
    callback: Callable | None = None
):

    estatisticas = Estatisticas()

    arquivos = sorted(
        pasta.glob("*.pdf")
    )

    estatisticas.total_arquivos = len(arquivos)

    resultados = []

    for pdf in arquivos:

        resultado = processar_pdf(pdf)

        resultados.append(resultado)

        if resultado.status == "Sucesso":
            estatisticas.sucessos += 1

        elif resultado.status == "NF não localizada":
            estatisticas.nao_encontrados += 1

        else:
            estatisticas.erros += 1

        if callback:
            callback(
                resultado,
                estatisticas
            )

    return resultados, estatisticas