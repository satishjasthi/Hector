from fastapi import FastAPI, File, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from hector.ocr_module.ocr_engine import OCR
from utils import convert_image_io_to_cv_img_rgb
app = FastAPI()
ocr_engine = OCR()

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request:Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"id": id}
    )


#################################################### OCR endpoints ####################################################

@app.post('/actions/ocr/extract_text_from_image')
async def extract_text_from_image(image:UploadFile = File(...)):
    try:
        contents = await image.read()
        img_rgb = convert_image_io_to_cv_img_rgb(contents)
        text_extracted = ocr_engine.extract_text(img_rgb)
        return text_extracted
    except Exception as e:
        return {"error": f"An error occurred: {e}"}


########################################################################################################################