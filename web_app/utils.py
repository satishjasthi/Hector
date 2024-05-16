import cv2
from io import BytesIO
import numpy as np

def convert_image_io_to_cv_img_rgb(image_data: BytesIO):
    image_array = np.asarray(bytearray(image_data), dtype=np.uint8)
    image_bgr = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    return image_rgb