import cv2
import numpy as np

from dlib import shape_predictor

from filters.Filter import Filter

class Landmarks(Filter):
    NAME = "Landmarks"
    PREDICTOR_MODEL = "data/shape_predictor_68_face_landmarks.dat"

    def __init__(self, active=False):
        # TODO: remove width and height from here, we get it else where now
        super(Landmarks, self).__init__(Landmarks.NAME, active)

        self._pose_predictor = shape_predictor(Landmarks.PREDICTOR_MODEL)

    def process_frame(self, frame):
        if not self._sense == None:
            filter = super(Landmarks, self)

            # Get people in frame
            matches = self._sense.active_people()

            for _, person in matches.iteritems():
                landmarks = self._pose_predictor(frame, person.dlib_shape())
                landmarks = np.matrix([[p.x, p.y] for p in landmarks.parts()])
                for idx, point in enumerate(landmarks):
                    position = (point[0, 0], point[0, 1])
                    cv2.circle(frame, position, 3, color=(0, 255, 255))

        return frame
