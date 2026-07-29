from pathlib import Path
import zipfile

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/download")
def download():

    pasta_saida = Path("outputs")

    if not pasta_saida.exists():
        raise HTTPException(status_code=404, detail="Pasta de saída não encontrada.")

    pdfs = list(pasta_saida.glob("*.pdf"))

    if not pdfs:
        raise HTTPException(status_code=404, detail="Nenhum PDF encontrado.")

    arquivo_zip = pasta_saida / "Arquivos_Renomeados.zip"

    if arquivo_zip.exists():
        arquivo_zip.unlink()

    with zipfile.ZipFile(
        arquivo_zip,
        mode="w",
        compression=zipfile.ZIP_DEFLATED
    ) as zipf:

        for pdf in pdfs:
            zipf.write(pdf, arcname=pdf.name)

    return FileResponse(
        path=arquivo_zip,
        filename="Arquivos_Renomeados.zip",
        media_type="application/zip"
    )