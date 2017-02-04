from collections import namedtuple


class Eye(object):

    Position = namedtuple('Position', ['x', 'y', 'width', 'height'])

    def __init__(self, (x, y, width, height)):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    def centroid(self):
        return self._x + int(self._width / 2), self._y + int(self._height / 2)

    def shape(self):
        return Eye.Position(self._x, self._y, self._width, self._height)
