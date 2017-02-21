
class Filter(object):

    def __init__(self, width, height, name, sense, active=False):
        self._width = width
        self._height = height
        self._name = name
        self._sense = sense
        self._is_active = active
        pass

    def set_sense(self, sense):
        self._sense = sense

    def set_active(self, is_active):
        self._is_active = is_active

    def is_active(self):
        return self._is_active

    def apply(self, frame):
        if self._is_active:
            return self.process_frame(frame)
        return frame

    def process_frame(self, frame):
        return frame

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

    def name(self):
        return self._name
