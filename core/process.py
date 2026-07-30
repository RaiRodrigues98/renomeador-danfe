from pathlib import Path

from core.image import recortar_numero_nota
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
        # Converte a primeira página do PDF para imagem
        imagem = pdf_para_imagem(pdf_path)

        # Recorta somente a região onde normalmente aparece a NF
        recorte = recortar_numero_nota(imagem)

        # O leitor já possui uma tentativa original e uma tratada
        numero = ler_numero_nf(recorte)

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
            destino = pdf_path.with_name(novo_nome)

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

    return resultados, estatisticas