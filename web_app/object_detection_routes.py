from fastapi import APIRouter, File, UploadFile
from hector.object_detection.detectron import ObjectDetector
import numpy as np
import cv2

router = APIRouter()
obj_detector = ObjectDetector()

@router.post("/detect_generic_objects_from_image")
async def detect_common_objects_from_image(image: UploadFile = File(...)):
    try:
        contents = await image.read()
        image_array = np.asarray(bytearray(contents), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)  
        results = obj_detector.detect_objects(image)
        return {"detections": results}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}
