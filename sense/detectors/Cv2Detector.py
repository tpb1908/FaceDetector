import os
import time

import cv2

from sense.Face import Face
from sense.Eye import Eye
from sense.detectors.Detector import Detector


class Cv2Detector(Detector):
    # Source: https://github.com/opencv/opencv/tree/master/data/haarcascades
    FACE_HAAR_CASCADE_FACE_XML = "/cascades/haarcascade_frontalface_default.xml"
    EYE_HAAR_CASCADE_FACE_XML = "/cascades/haarcascade_eye.xml"

    def __init__(self):
        super(Cv2Detector, self).__init__()

        # Load cascade
        self.face_cascade = cv2.CascadeClassifier()
        self.eye_cascade = cv2.CascadeClassifier()
        assert self.face_cascade.load(os.getcwd() + Cv2Detector.FACE_HAAR_CASCADE_FACE_XML)
        assert self.eye_cascade.load(os.getcwd() + Cv2Detector.EYE_HAAR_CASCADE_FACE_XML)

    def get_faces(self, frame):
        start = time.time()
        # Get face positions
        img_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(img_grey, 1.3, 5)

        # Map positions to face objects
        faces = [Face(position, img_grey) for position in faces]
        print("CV2 detect: " + str(1000*(time.time() - start)))
        return faces

    def get_eyes(self, frame):
        img_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, frame, cv2.COLOR_BGR2GRAY)
        return [Eye(position) for position in self.eye_cascade.detectMultiScale(img_grey, 1.3, 5)]



