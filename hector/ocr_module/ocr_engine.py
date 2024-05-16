import easyocr
from pathlib import Path
from memory_profiler import profile


class OCR:
    # @profile
    def __init__(self) -> None:
        self.reader = easyocr.Reader(lang_list = ['en'])

    # @profile
    def extract_text(self, image:Path):
        """
        Extract text from image
        """
        data = self.reader.readtext(image)
        result = ''
        for bbox, text, cnf in data:
            result += ' ' + text
        return result
    

