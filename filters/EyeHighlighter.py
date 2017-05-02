import cv2

from filters.Filter import Filter
from ui.Painter import Painter

class EyeHighlighter(Filter):
    NAME = "Eye Highlighter"

    BOUNDING_BOX_COLOUR = (95, 120, 160)

    def __init__(self, active=False):
        super(EyeHighlighter, self).__init__(EyeHighlighter.NAME, active)

    def process_frame(self, frame):
        if self._sense is not None:
            eyes = self._sense.eyes()
            for eye in eyes:
                shape = eye.shape()
                Painter.rectangle(frame,
                                  shape.x,
                                  shape.y,
                                  shape.x + shape.width -1,
                                  shape.y + shape.height - 1,
                                  EyeHighlighter.BOUNDING_BOX_COLOUR,
                                  1)
        return frame
