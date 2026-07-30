import zipfile
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from utils.files import pasta_sessao

router = APIRouter()


@router.get("/download/{sessao_id}")
def download(sessao_id: str):
    try:
        pasta = pasta_sessao(sessao_id)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro

    pasta_saida = pasta / "saida"
    pdfs = sorted(pasta_saida.glob("*.pdf")) if pasta_saida.exists() else []
    if not pdfs:
        raise HTTPException(status_code=404, detail="Nenhum PDF processado com sucesso.")

    arquivo_zip = pasta / "Arquivos_Renomeados.zip"
    with zipfile.ZipFile(arquivo_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for pdf in pdfs:
            zipf.write(pdf, arcname=pdf.name)

    return FileResponse(
        path=arquivo_zip,
        filename="Arquivos_Renomeados.zip",
        media_type="application/zip",
    )
