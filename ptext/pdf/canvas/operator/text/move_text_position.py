import copy
from decimal import Decimal
from typing import List

from ptext.exception.pdf_exception import PDFTypeError
from ptext.io.transform.types import AnyPDFType
from ptext.pdf.canvas.geometry.matrix import Matrix
from ptext.pdf.canvas.operator.canvas_operator import CanvasOperator


class MoveTextPosition(CanvasOperator):
    """
    Move to the start of the next line, offset from the start of the current line by
    (tx , ty). t x and t y shall denote numbers expressed in unscaled text space
    units. More precisely, this operator shall perform these assignments:
    Tm = Tlm = [[1,0,0], [0,1,0],[tx,ty,1]] * Tlm
    """

    def __init__(self):
        super().__init__("Td", 2)

    def invoke(self, canvas: "Canvas", operands: List[AnyPDFType] = []):

        if not isinstance(operands[0], Decimal):
            raise PDFTypeError(
                expected_type=Decimal, received_type=operands[0].__class__
            )
        if not isinstance(operands[1], Decimal):
            raise PDFTypeError(
                expected_type=Decimal, received_type=operands[1].__class__
            )

        tx = operands[0]
        ty = operands[1]

        m = Matrix.identity_matrix()
        m[2][0] = tx
        m[2][1] = ty

        canvas.graphics_state.text_matrix = m.mul(
            canvas.graphics_state.text_line_matrix
        )
        canvas.graphics_state.text_line_matrix = copy.deepcopy(
            canvas.graphics_state.text_matrix
        )
