from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routes.download import router as download_router
from routes.processar import router as processar_router

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Renomeador DANFE")

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)

app.include_router(processar_router)
app.include_router(download_router)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )