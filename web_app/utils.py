from fastapi import File, UploadFile
import cv2
import numpy as np

def convert_image_io_to_cv_img_rgb(image_content):
    # Convert to NumPy array
    img_array = cv2.imdecode(np.frombuffer(image_content, np.uint8), cv2.IMREAD_COLOR)

    # Convert to RGB format (EasyOCR expects RGB)
    return  cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
