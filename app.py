from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes.download import router as download_router
from routes.processar import router as processar_router

app = FastAPI(title="Renomeador DANFE")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(processar_router)
app.include_router(download_router)
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        }
    )