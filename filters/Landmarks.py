import cv2
import numpy as np

from dlib import shape_predictor

from filters.Filter import Filter


class Landmarks(Filter):
    NAME = "Landmarks"
    PREDICTOR_MODEL = "data/dlib_shape.dat"
    POSE_PREDICTOR = shape_predictor(PREDICTOR_MODEL)

    def __init__(self, active=False):
        super(Landmarks, self).__init__(Landmarks.NAME, active)

    def process_frame(self, frame):
        if self._sense is not None:

            # Get people in frame
            matches = self._sense.active_people()

            for _, person in matches.iteritems():
                # Get landmarks
                landmarks = Landmarks.POSE_PREDICTOR(frame, person.dlib_shape())
                person.face().landmarks = landmarks

                # Draw landmarks
                landmarks = np.matrix([[p.x, p.y] for p in landmarks.parts()])

                last = None
                start = None
                for idx, point in enumerate(landmarks):
                    if last is None:
                        start = point[0]
                    else:
                        cv2.line(frame, (point.item(0), point.item(1)), (last.item(0), last.item(1)), (0, 255, 0), 1)
                    position = (point[0, 0], point[0, 1])
                    cv2.circle(frame, position, 3, color=(0, 255, 255))
                    # http://openface-api.readthedocs.io/en/latest/_images/dlib-landmark-mean.png
                    if idx == 30:
                        start = point[0]
                        last = point[0]
                    elif idx in [16, 21, 26]:
                        last = None
                    elif idx in [35, 41, 47, 67]:
                        last = None
                        cv2.line(frame, (point.item(0), point.item(1)), (start.item(0), start.item(1)), (0, 255, 0), 1)
                    else:
                        last = point[0]

        return frame
