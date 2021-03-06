from typing import List

from ptext.action.structure.line.line_render_event import (
    LineRenderEvent,
)
from ptext.pdf.canvas.geometry.rectangle import Rectangle


class ParagraphRenderEvent(LineRenderEvent):
    def __init__(self, line_render_events: List[LineRenderEvent]):
        super(ParagraphRenderEvent, self).__init__(line_render_events)

    def get_text(self) -> str:
        return "".join([x.get_text() + "\n" for x in self.contained_events])

    def get_bounding_box(self) -> Rectangle:
        top = (
            self.contained_events[0].get_bounding_box().y
            + self.contained_events[0].get_bounding_box().height
        )
        btm = self.contained_events[-1].get_bounding_box().y
        left = min([x.get_bounding_box().x for x in self.contained_events])
        right = max(
            [
                x.get_bounding_box().x + x.get_bounding_box().width
                for x in self.contained_events
            ]
        )
        return Rectangle(left, btm, (right - left), (top - btm))
