import openface
import dlib
import os
from skimage.io import imsave

from filters.Filter import Filter
from filters.Landmarks import Landmarks
import modes.Capture as Capture


class FaceTransform(Filter):
    NAME = "Face Transform"
    FACE_ALIGNER = openface.AlignDlib(Landmarks.PREDICTOR_MODEL)

    def __init__(self, active=False):
        super(FaceTransform, self).__init__(FaceTransform.NAME, active)
        self.ctr = 0
        self.enrollee = None

    def process_frame(self, frame):
        if self._sense is not None:

            # Get people in frame
            people = self._sense.active_people()
            idx = 0
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

                if shape.width + x > self.width or x < 0 : break
                if shape.height + y > self.height or y < 0: break
                frame[y:y + aligned.shape[0], x:x + aligned.shape[1], 0] = aligned
                frame[y:y + aligned.shape[0], x:x + aligned.shape[1], 1] = aligned
                frame[y:y + aligned.shape[0], x:x + aligned.shape[1], 2] = aligned
                if idx == 0 and self._mode.NAME == Capture.Capture.NAME and self._mode.enrollee() is not None:
                    self.save_image(aligned)
                idx += 1

        return frame

    def save_image(self, aligned):
        enrollee = self._mode.enrollee()
        if self.enrollee != enrollee:
            self.ctr = 0
            self.enrollee = enrollee
            if not os.path.exists(enrollee):
                os.makedirs("person_{}".format(enrollee))
            path, dirs, files = os.walk("person_{}".format(enrollee)).next()
            self.ctr = len(files)
        imsave(os.path.join(self._mode.enrollee(), "{}_.png".format(self.ctr)), aligned)
        self.ctr += 1

