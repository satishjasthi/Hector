from pathlib import Path
from fastapi import APIRouter, File, UploadFile
from hector.image_metadata.metadata_extractors import fetch_image_metadata

router = APIRouter()


@router.post("/extract_image_metadata")
async def extract_metadata_from_image(image: UploadFile = File(...)):
    try:
        filename = Path(f"/tmp/{image.filename}")
        image_content = await image.read()
        with open(filename, "w") as f:
            f.write(image_content)
        img_metadata = fetch_image_metadata(filename)
        filename.unlink()
        return img_metadata
    except Exception as e:
        return {"error": f"An error occurred: {e}"}