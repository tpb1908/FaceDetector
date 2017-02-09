import cv2
import dlib
import time

from sense.Face import Face
from sense.detectors.Detector import Detector


class DlibDetector(Detector):
    def __init__(self):
        super(DlibDetector, self).__init__()

        # Create face detector
        self._detector = dlib.get_frontal_face_detector()

    def get_faces(self, frame):
        start = time.time()
        img_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Get all faces in frame
        faces = []
        for position in self._detector(frame, 1):
            # Convert position into (x, y, width, height)
            top, left, bottom, right = position.top(), position.left(), position.bottom(), position.right()
            face_position = (left, top, right - left, bottom - top)

            faces.append(Face(face_position, img_grey))
        print("Dlib detect: " + str(1000*(time.time() - start)))
        return faces

