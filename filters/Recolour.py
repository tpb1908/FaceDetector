from cv2 import cvtColor, COLOR_BGR2RGBA

from Filter import Filter


class Recolour(Filter):

    def __init__(self, width, height):
        super(Recolour, self).__init__(width, height)

    def apply(self, frame):
        return cvtColor(frame, COLOR_BGR2RGBA)
