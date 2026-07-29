from pathlib import Path
import zipfile

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from config import OUTPUT_DIR

router = APIRouter()


@router.get("/download")
def download():

    if not OUTPUT_DIR.exists():
        raise HTTPException(
            status_code=404,
            detail="Pasta de saída não encontrada."
        )

    pdfs = sorted(
        OUTPUT_DIR.glob("*.pdf")
    )

    if not pdfs:
        raise HTTPException(
            status_code=404,
            detail="Nenhum PDF encontrado."
        )

    arquivo_zip = OUTPUT_DIR / "Arquivos_Renomeados.zip"

    if arquivo_zip.exists():
        arquivo_zip.unlink()

    with zipfile.ZipFile(
        arquivo_zip,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zipf:

        for pdf in pdfs:
            zipf.write(
                pdf,
                arcname=pdf.name
            )

    return FileResponse(
        path=arquivo_zip,
        filename="Arquivos_Renomeados.zip",
        media_type="application/zip"
    )