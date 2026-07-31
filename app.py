from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routes.download import router as download_router
from routes.processar import router as processar_router
from utils.files import limpar_sessoes_antigas
from utils.logger import logger

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(_: FastAPI):
    limpar_sessoes_antigas()
    logger.info("Renomeador DANFE v5.0 iniciado")
    yield
    logger.info("Renomeador DANFE v5.0 finalizado")


app = FastAPI(
    title="Renomeador DANFE",
    version="5.0.0",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.include_router(processar_router)
app.include_router(download_router)


@app.get("/", include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health", include_in_schema=False)
def health() -> JSONResponse:
    return JSONResponse({"status": "ok", "version": "5.0.0"})
