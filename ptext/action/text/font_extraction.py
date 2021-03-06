from typing import List

from ptext.pdf.canvas.event.begin_page_event import BeginPageEvent
from ptext.pdf.canvas.event.event_listener import EventListener, Event


class FontExtraction(EventListener):
    def __init__(self):
        self.fonts_per_page = {}
        self.current_page = -1

    def event_occurred(self, event: "Event") -> None:
        if isinstance(event, BeginPageEvent):
            self._begin_page(event)

    def _begin_page(self, event: "BeginPageEvent"):

        # update page number
        self.current_page += 1
        self.fonts_per_page[self.current_page] = []

        # get page
        page = event.get_page()
        if page is None:
            return

        # get resources
        if "Resources" not in page or not isinstance(page["Resources"], dict):
            return
        if "Font" not in page["Resources"] or not isinstance(
            page["Resources"]["Font"], dict
        ):
            return

        for _, f in page["Resources"]["Font"].items():
            self.fonts_per_page[self.current_page].append(f)

    def get_fonts_per_page(self, page_number: int) -> List["Font"]:
        return (
            self.fonts_per_page[page_number]
            if page_number in self.fonts_per_page
            else []
        )

    def get_font_names_per_page(self, page_number: int) -> List[str]:
        return [x.get_font_name() for x in self.get_fonts_per_page(page_number)]
