from fastapi import APIRouter, File, UploadFile
from hector.ocr_module.ocr_engine import OCR
from .utils import convert_image_io_to_cv_img_rgb

router = APIRouter()
ocr_engine = OCR()

@router.post("/extract_text_from_image")
async def extract_text_from_image(image: UploadFile = File(...)):
    try:
        contents = await image.read()
        img_rgb = convert_image_io_to_cv_img_rgb(contents)
        text_extracted = ocr_engine.extract_text(img_rgb)
        return text_extracted
    except Exception as e:
        return {"error": f"An error occurred: {e}"}
