import cv2
import dlib
import time

from sense.Face import Face
from sense.detection.Detection import Detection


class DlibDetection(Detection):
    def __init__(self):
        super(DlibDetection, self).__init__()

        # Create face detector
        self._detector = dlib.get_frontal_face_detector()
        self._last_update_time = 0

    def get_faces(self, frame):
        start = time.time()
        img_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Reduce image size to speed up detector
        percentage_size = 0.5
        small_img = cv2.resize(img_grey, (0, 0), fx=percentage_size, fy=percentage_size)

        offset = int(1 / percentage_size)
        # Get all faces in frame
        faces = []
        for position in self._detector(small_img, 1):
            # Convert position into (x, y, width, height)
            top, left, bottom, right = position.top(), position.left(), position.bottom(), position.right()
            face_position = (left * offset, top * offset,
                             (right - left) * offset, (bottom - top) * offset)
            if left > 0 and top > 0 and bottom < frame.shape[1] and right < frame.shape[0]:
                faces.append(Face(face_position, img_grey))
        self._last_update_time = 1000 * (time.time() - start)
        return faces

    def detect_time(self):
        return self._last_update_time
