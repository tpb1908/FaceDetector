import cv2
import os

from sense.Face import Face

class Cv2Detection(object):
    # Source: https://github.com/opencv/opencv/tree/master/data/haarcascades
    HAAR_CASCADE_FACE_XML = "/cascades/haarcascade_frontalface_default.xml"

    def __init__(self):
        # Load cascade
        self.face_cascade = cv2.CascadeClassifier()
        assert self.face_cascade.load(os.getcwd() + Cv2Detection.HAAR_CASCADE_FACE_XML)
        
    def get_faces(self, frame):
        # Get face positions
        img_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(img_grey, 1.3, 5)
        
        # Map positions to face objects
        faces = [Face(position, img_grey) for position in faces]

        return faces