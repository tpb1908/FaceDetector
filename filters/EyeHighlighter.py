import cv2

from filters.Filter import Filter


class EyeHighlighter(Filter):

    NAME = "Eye Highlighter"

    BOUNDING_BOX_COLOUR = (95, 120, 160)

    def __init__(self, width, height, sense, active=False):
        super(EyeHighlighter, self).__init__(width, height, EyeHighlighter.NAME, sense, active)
        
    def process_frame(self, frame):
        # self._sense.process_eyes(frame)
        eyes = self._sense.get_eyes()
        for eye in eyes:
            shape = eye.shape()
            cv2.rectangle(frame,
                          (shape.x, shape.y),
                          (shape.x + shape.width - 1, shape.y + shape.height - 1),
                          EyeHighlighter.BOUNDING_BOX_COLOUR,
                          1)
        return frame
