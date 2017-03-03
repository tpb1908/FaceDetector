from cv2 import cvtColor, COLOR_BGR2RGBA

from Filter import Filter


class Recolour(Filter):
    NAME = "Recolour"

    def __init__(self, active=False):
        super(Recolour, self).__init__(Recolour.NAME, active)

    def process_frame(self, frame):
        return cvtColor(frame, COLOR_BGR2RGBA)
