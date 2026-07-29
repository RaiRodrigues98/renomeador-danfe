from pathlib import Path
import shutil

from fastapi import APIRouter, File, UploadFile

from config import OUTPUT_DIR, UPLOAD_DIR
from core.process import processar_pdf

router = APIRouter()


@router.post("/processar")
async def processar(
    arquivos: list[UploadFile] = File(...)
):

    if UPLOAD_DIR.exists():
        shutil.rmtree(UPLOAD_DIR)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    resultados = []

    for arquivo in arquivos:

        destino = UPLOAD_DIR / arquivo.filename

        with open(destino, "wb") as buffer:
            shutil.copyfileobj(
                arquivo.file,
                buffer
            )

        resultado = processar_pdf(
            destino,
            OUTPUT_DIR
        )

        resultados.append(
            {
                "arquivo_original": resultado.arquivo_original,
                "arquivo_final": resultado.arquivo_final,
                "numero_nf": resultado.numero_nf,
                "status": resultado.status,
            }
        )

    return {
        "status": "ok",
        "resultados": resultados,
    }