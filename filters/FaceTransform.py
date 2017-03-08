import cv2
import openface
import dlib

from filters.Filter import Filter
from filters.Landmarks import Landmarks


class FaceTransform(Filter):
    NAME = "Face Transform"
    FACE_ALIGNER = openface.AlignDlib(Landmarks.PREDICTOR_MODEL)

    def __init__(self, active=False):
        super(FaceTransform, self).__init__(FaceTransform.NAME, active)

    def process_frame(self, frame):
        if self._sense is not None:

            # Get people in frame
            people = self._sense.active_people()

            for _, person in people.iteritems():
                # Get landmarks
                face = person.face()
                shape = face.shape()
                landmarks = face.landmarks
                if landmarks is None: break

                aligned = FaceTransform.FACE_ALIGNER.align(shape.width, face.uint8_image(),
                                                           dlib.rectangle(0, 0, shape.width, shape.width),
                                                           landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
                x = shape.x
                y = shape.y
                if shape.width + x > self.width or x < 0: break
                if shape.height + y > self.height or y < 0: break
                frame[y:y + aligned.shape[0], x:x + aligned.shape[1], 0] = aligned
                frame[y:y + aligned.shape[0], x:x + aligned.shape[1], 1] = aligned
                frame[y:y + aligned.shape[0], x:x + aligned.shape[1], 2] = aligned

        return frame
