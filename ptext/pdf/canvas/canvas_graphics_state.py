import copy
from decimal import Decimal

from ptext.pdf.canvas.color.color import RGBColor
from ptext.pdf.canvas.geometry.matrix import Matrix


class CanvasGraphicsState:
    """
    A conforming reader shall maintain an internal data structure called the graphics state that holds current
    graphics control parameters. These parameters define the global framework within which the graphics
    operators execute.

    EXAMPLE 1
    The f (fill) operator implicitly uses the current colour parameter, and the S (stroke) operator additionally
    uses the current line width parameter from the graphics state.

    A conforming reader shall initialize the graphic state at the beginning of each page with the values specified in
    Table 52 and Table 53. Table 52 lists those graphics state parameters that are device-independent and are
    appropriate to specify in page descriptions. The parameters listed in Table 53 control details of the rendering
    (scan conversion) process and are device-dependent; a page description that is intended to be device-
    independent should not be written to modify these parameters.
    """

    def __init__(self):
        self.ctm = Matrix.identity_matrix()
        self.text_matrix = Matrix.identity_matrix()
        self.text_line_matrix = Matrix.identity_matrix()
        self.text_rise = Decimal(0)
        self.character_spacing = Decimal(0)
        self.word_spacing = Decimal(0)
        self.horizontal_scaling = Decimal(100)
        self.leading = Decimal(0)
        self.font = None
        self.font_size = None
        self.clipping_path = None
        self.non_stroke_color_space = None
        self.non_stroke_color = RGBColor(Decimal(0), Decimal(0), Decimal(0))
        self.stroke_color_space = None
        self.stroke_color = RGBColor(Decimal(0), Decimal(0), Decimal(0))
        self.line_width = Decimal(1)
        self.line_cap = None
        self.line_join = None
        self.miter_limit = Decimal(10)
        self.dash_pattern = None
        self.rendering_intent = None
        self.stroke_adjustment = None
        self.blend_mode = None
        self.soft_mask = None
        self.alpha_constant = None
        self.alpha_source = None

    def __deepcopy__(self, memodict={}):
        out = CanvasGraphicsState()
        out.ctm = copy.deepcopy(self.ctm)
        out.text_matrix = copy.deepcopy(self.text_matrix)
        out.text_line_matrix = copy.deepcopy(self.text_line_matrix)
        out.text_rise = self.text_rise
        out.character_spacing = self.character_spacing
        out.word_spacing = self.word_spacing
        out.horizontal_scaling = self.horizontal_scaling
        out.leading = self.leading
        out.font = copy.deepcopy(self.font)
        out.font_size = self.font_size
        # out.clipping_path = None
        # out.non_stroke_color_space = None
        out.non_stroke_color = copy.deepcopy(self.non_stroke_color)
        # out.stroke_color_space = None
        out.stroke_color = copy.deepcopy(self.stroke_color)
        out.line_width = self.line_width
        # self.line_cap = None
        # self.line_join = None
        out.miter_limit = self.miter_limit
        # self.dash_pattern = None
        # self.rendering_intent = None
        # self.stroke_adjustment = None
        # self.blend_mode = None
        # self.soft_mask = None
        # self.alpha_constant = None
        # self.alpha_source = None
        return out
