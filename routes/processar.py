from fastapi import APIRouter, UploadFile, File
from pathlib import Path
import shutil

from core.processor import processar_pdf

router = APIRouter()


@router.post("/processar")
async def processar(arquivos: list[UploadFile] = File(...)):

    pasta_upload = Path("uploads")
    pasta_saida = Path("outputs")

    # Limpa as pastas da execução anterior
    if pasta_upload.exists():
        shutil.rmtree(pasta_upload)

    if pasta_saida.exists():
        shutil.rmtree(pasta_saida)

    # Recria as pastas
    pasta_upload.mkdir(parents=True, exist_ok=True)
    pasta_saida.mkdir(parents=True, exist_ok=True)

    resultados = []

    for arquivo in arquivos:

        destino = pasta_upload / arquivo.filename

        with open(destino, "wb") as buffer:
            shutil.copyfileobj(arquivo.file, buffer)

        resultado = processar_pdf(
            destino,
            pasta_saida
        )

        resultados.append({
            "arquivo_original": resultado.arquivo_original,
            "arquivo_final": resultado.arquivo_final,
            "numero_nf": resultado.numero_nf,
            "status": resultado.status
        })

    return {
        "status": "ok",
        "resultados": resultados
    }