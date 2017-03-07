import cv2
import numpy as np

from dlib import shape_predictor

from filters.Filter import Filter

class Landmarks(Filter):
    NAME = "Landmarks"
    PREDICTOR_MODEL = "data/shape_predictor_68_face_landmarks.dat"
    POSE_PREDICTOR = shape_predictor(PREDICTOR_MODEL)

    def __init__(self, active=False):
        super(Landmarks, self).__init__(Landmarks.NAME, active)

    def process_frame(self, frame):
        if not self._sense == None:
            filter = super(Landmarks, self)

            # Get people in frame
            matches = self._sense.active_people()

            for _, person in matches.iteritems():
                # Get landmarks
                landmarks = Landmarks.POSE_PREDICTOR(frame, person.dlib_shape())
                person.face().landmarks = landmarks

                # Draw landmarks
                landmarks = np.matrix([[p.x, p.y] for p in landmarks.parts()])

                last = None
                for idx, point in enumerate(landmarks):
                    if last is not None:
                        cv2.line(frame, (point.item(0), point.item(1)), (last.item(0), last.item(1)), (0, 255, 0), 1)
                    position = (point[0, 0], point[0, 1])
                    cv2.circle(frame, position, 3, color=(0, 255, 255))
                    # http://openface-api.readthedocs.io/en/latest/_images/dlib-landmark-mean.png
                    if idx in [16, 21, 26, 30, 35, 41, 47, 67]:
                        last = None
                    else:
                        last = point[0]

        return frame
