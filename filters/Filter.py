class Filter(object):

    def __init__(self, width, height):
        self._width = width
        self._height = height
        pass

    def apply(self, frame):
        return frame

    def width(self):
        return self._width

    def height(self):
        return self._height
