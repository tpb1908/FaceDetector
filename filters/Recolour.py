from cv2 import cvtColor, COLOR_BGR2RGBA

from Filter import Filter


class Recolour(Filter):
    NAME = "Recolour"

    def __init__(self, width, height):
        super(Recolour, self).__init__(width, height, Recolour.NAME)

    def apply(self, frame):
        return cvtColor(frame, COLOR_BGR2RGBA)
