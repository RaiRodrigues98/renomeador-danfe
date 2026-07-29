from pathlib import Path

import cv2

from core.image import (
    melhorar_imagem,
    recortar_numero_nota,
)
from core.leitor_nf import ler_numero_nf
from core.models import ResultadoProcessamento
from core.pdf import pdf_para_imagem
from core.statistics import Estatisticas

from utils.files import renomear_arquivo
from utils.logger import logger


def processar_pdf(
    pdf_path: Path,
    pasta_saida: Path | None = None
) -> ResultadoProcessamento:

    logger.info(f"Processando: {pdf_path.name}")

    try:

        # Converte PDF para imagem
        imagem = pdf_para_imagem(pdf_path)

        cv2.imwrite("debug_pagina.png", imagem)

        # Recorta a região da NF
        recorte = recortar_numero_nota(imagem)

        cv2.imwrite("debug_recorte.png", recorte)

        # Primeira tentativa (imagem original)
        numero = ler_numero_nf(recorte)

        # Segunda tentativa (imagem tratada)
        if numero is None:

            imagem_tratada = melhorar_imagem(recorte)

            cv2.imwrite(
                "debug_tratada.png",
                imagem_tratada
            )

            numero = ler_numero_nf(imagem_tratada)

        # Não encontrou
        if numero is None:

            return ResultadoProcessamento(
                arquivo_original=pdf_path.name,
                arquivo_final=None,
                numero_nf=None,
                status="NF não localizada"
            )

        novo_nome = f"{numero}.pdf"

        if pasta_saida:

            pasta_saida.mkdir(
                parents=True,
                exist_ok=True
            )

            destino = pasta_saida / novo_nome

        else:

            destino = pdf_path.with_name(
                novo_nome
            )

        destino = renomear_arquivo(
            pdf_path,
            destino
        )

        return ResultadoProcessamento(
            arquivo_original=pdf_path.name,
            arquivo_final=destino.name,
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
    callback=None
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

    return resultados, estatisticasok