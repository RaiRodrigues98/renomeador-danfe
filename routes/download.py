import zipfile

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
    pdfs = sorted(pasta_saida.glob("*.pdf")) if pasta_saida.is_dir() else []
    if not pdfs:
        raise HTTPException(status_code=404, detail="Nenhum PDF processado com sucesso.")

    arquivo_zip = pasta / "Arquivos_Renomeados.zip"
    temporario = pasta / ".Arquivos_Renomeados.tmp"
    with zipfile.ZipFile(temporario, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zipf:
        for pdf in pdfs:
            zipf.write(pdf, arcname=pdf.name)
    temporario.replace(arquivo_zip)

    return FileResponse(
        path=arquivo_zip,
        filename="Arquivos_Renomeados.zip",
        media_type="application/zip",
    )
