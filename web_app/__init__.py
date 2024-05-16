from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .ocr_routes import router as ocr_router
from .object_detection_routes import router as detection_router

app = FastAPI()
# app.mount("/static", StaticFiles(directory="static"), name="static")  # Assuming you have a 'static' folder for CSS, JS, etc.
templates = Jinja2Templates(directory="templates")

app.include_router(ocr_router, prefix="/actions/ocr")
app.include_router(detection_router, prefix="/actions/object_detection")

@app.get("/")
async def root(request):
    return templates.TemplateResponse("index.html", {"request": request})
