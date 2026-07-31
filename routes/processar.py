import asyncio
import uuid
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from config import MAX_CONCURRENT_OCR, MAX_UPLOAD_MB
from core.process import processar_pdf
from utils.files import limpar_sessoes_antigas, nome_seguro, pasta_sessao

router = APIRouter()
_CHUNK_SIZE = 1024 * 1024
_PROCESSING_LIMIT = asyncio.Semaphore(MAX_CONCURRENT_OCR)


@router.post("/sessao")
def criar_sessao() -> dict:
    limpar_sessoes_antigas()
    sessao_id = uuid.uuid4().hex
    pasta = pasta_sessao(sessao_id)
    (pasta / "entrada").mkdir(parents=True, exist_ok=False)
    (pasta / "saida").mkdir(parents=True, exist_ok=False)
    return {"sessao_id": sessao_id}


async def _salvar_upload(arquivo: UploadFile, destino: Path) -> None:
    limite = MAX_UPLOAD_MB * 1024 * 1024
    total = 0
    try:
        with destino.open("xb") as saida:
            while bloco := await arquivo.read(_CHUNK_SIZE):
                total += len(bloco)
                if total > limite:
                    raise HTTPException(
                        status_code=413,
                        detail=f"Arquivo maior que {MAX_UPLOAD_MB} MB.",
                    )
                saida.write(bloco)
    except Exception:
        destino.unlink(missing_ok=True)
        raise
    finally:
        await arquivo.close()


@router.post("/processar-arquivo")
async def processar_arquivo(
    sessao_id: str = Form(...),
    arquivo: UploadFile = File(...),
) -> dict:
    if not arquivo.filename:
        raise HTTPException(status_code=400, detail="Arquivo sem nome.")
    if not arquivo.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="O arquivo precisa ser PDF.")

    try:
        pasta = pasta_sessao(sessao_id)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro
    if not pasta.is_dir():
        raise HTTPException(status_code=404, detail="Sessão não encontrada ou expirada.")

    nome = nome_seguro(arquivo.filename)
    caminho_pdf = pasta / "entrada" / f"{uuid.uuid4().hex}_{nome}"
    await _salvar_upload(arquivo, caminho_pdf)

    async with _PROCESSING_LIMIT:
        resultado = await asyncio.to_thread(processar_pdf, caminho_pdf, pasta / "saida")
    # Preserva o nome original exibido pela interface.
    resultado.arquivo_original = nome
    return resultado.to_dict()
