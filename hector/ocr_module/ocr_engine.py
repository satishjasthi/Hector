from typing import Union
import easyocr
from pathlib import Path
from memory_profiler import profile
import numpy as np

class OCR:
    # @profile
    def __init__(self) -> None:
        self.reader = easyocr.Reader(lang_list = ['en'])

    # @profile
    def extract_text(self, image:Union[Path,np.ndarray]):
        """
        Extract text from image
        """
        data = self.reader.readtext(image)
        result = ''
        for bbox, text, cnf in data:
            result += ' ' + text
        return result
    

