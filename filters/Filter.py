class Filter(object):

    def __init__(self, width, height, name):
        self._width = width
        self._height = height
        self._name = name
        pass

    def apply(self, frame):
        return frame

    def width(self):
        return self._width

    def height(self):
        return self._height

    def name(self):
        return self._name