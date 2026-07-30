from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routes.download import router as download_router
from routes.processar import router as processar_router
from utils.files import limpar_sessoes_antigas

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(_: FastAPI):
    limpar_sessoes_antigas()
    yield


app = FastAPI(title="Renomeador DANFE", version="3.0.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.include_router(processar_router)
app.include_router(download_router)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
