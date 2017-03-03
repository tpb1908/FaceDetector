import time
import dlib

class Person(object):
    def __init__(self, face, name):
        self._prev_face = face
        self._face = face

        self._last_seen = time.time()
        self._count = 0
        self._name = name

    def update(self, face):
        # Update face
        self._prev_face = self._face
        self._face = face

        # Update time stamp
        self._last_seen = time.time()

    def has_crossed(self, line_y):
        prev_x, prev_y = self._prev_face.centroid()
        x, y = self._face.centroid()
        cross_down = y > line_y > prev_y
        cross_up = y < line_y < prev_y
        return cross_down or cross_up

    def shape(self):
        return self._face.shape()

    # Returns a dlib rectange representing the position of the face
    def dlib_shape(self):
        shape = self.shape()
        return dlib.rectangle(long(shape.x), long(shape.y), 
            long(shape.x + shape.width), long(shape.y + shape.height))

    def centroid(self):
        return self._face.centroid()

    def active(self):
        return self._last_seen + 3 > time.time()

    def increment(self):
        self._count += 1

    def count(self):
        return self._count

    def name(self):
        return self._name
