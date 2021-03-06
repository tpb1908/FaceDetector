import os
import time

import cv2

from sense.Face import Face
from sense.Eye import Eye
from sense.detection.Detection import Detection


class Cv2Detection(Detection):
    # Source: https://github.com/opencv/opencv/tree/master/data/haarcascades
    FACE_HAAR_CASCADE_FACE_XML = "/cascades/haarcascade_frontalface_default.xml"
    EYE_HAAR_CASCADE_FACE_XML = "/cascades/haarcascade_eye.xml"

    def __init__(self):
        super(Cv2Detection, self).__init__()

        # Load cascade
        self.face_cascade = cv2.CascadeClassifier()
        self.eye_cascade = cv2.CascadeClassifier()
        assert self.face_cascade.load(os.getcwd() + Cv2Detection.FACE_HAAR_CASCADE_FACE_XML)
        assert self.eye_cascade.load(os.getcwd() + Cv2Detection.EYE_HAAR_CASCADE_FACE_XML)
        self._last_update_time = 0

    def get_faces(self, frame):
        start = time.time()
        
        # Get face positions
        img_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(img_grey, 1.3, 5)

        # Map positions to face objects
        faces = [Face(position, img_grey) for position in faces]

        self._last_update_time = 1000*(time.time() - start)
        return faces

    def get_eyes(self, frame):
        img_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, frame, cv2.COLOR_BGR2GRAY)
        return [Eye(position) for position in self.eye_cascade.detectMultiScale(img_grey, 1.3, 5)]

    def detect_time(self):
        return self._last_update_time

