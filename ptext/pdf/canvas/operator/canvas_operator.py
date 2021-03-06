from typing import List

from ptext.io.transform.types import AnyPDFType


class CanvasOperator:
    def __init__(self, text: str, number_of_operands: int):
        self.text = text
        self.number_of_operands = number_of_operands

    def get_text(self) -> str:
        return self.text

    def get_number_of_operands(self) -> int:
        return self.number_of_operands

    def invoke(self, canvas: "PDFCanvas", operands: List[AnyPDFType] = []):
        pass
