from typing import List

from ptext.io.transform.types import AnyPDFType
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class BeginCompatibilitySection(CanvasOperator):
    """
    (PDF 1.1) Begin a compatibility section. Unrecognized operators (along with
    their operands) shall be ignored without error until the balancing EX operator
    is encountered.
    """

    def __init__(self):
        super().__init__("BX", 0)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []):
        canvas.in_compatibility_section = True
