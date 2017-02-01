import time

class Person(object):
    def __init__(self, face, name):
        self._face = face
        self._last_seen = time.time()
        self._count = 0
        self._name = name

    def update(self, face):
        self._face = face
        self._last_seen = time.time()

    def shape(self):
        return self._face.shape()