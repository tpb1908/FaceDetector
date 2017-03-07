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
        if not self._sense == None:

            # Get people in frame
            people = self._sense.active_people()

            for _, person in people.iteritems():
                # Get landmarks
                landmarks = person.face().landmarks
                if landmarks is None: break
                d = person.face().dlib_rect()
                print(person.face().shape())
                print(" Left: {} Top: {} Right: {} Bottom: {}".format(
                d.left(), d.top(), d.right(), d.bottom())) 
                print(person.face().image().sum())
                cv2.imwrite("test.jpg", person.face().image())
                
                aligned = FaceTransform.FACE_ALIGNER.align(person.face().shape().width, person.face().uint8_image(), dlib.rectangle(0, 0, person.face().shape().width, person.face().shape().width), landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
                x = person.face().shape().x
                y = person.face().shape().y
                if((person.shape().width + x > self.width) or x < 0): break
                if((person.shape().height + y > self.height) or y < 0): break
                frame[y:y+aligned.shape[0], x:x+aligned.shape[1], 0] = aligned
                frame[y:y+aligned.shape[0], x:x+aligned.shape[1], 1] = aligned
                frame[y:y+aligned.shape[0], x:x+aligned.shape[1], 2] = aligned
                # cv2.imwrite("test.jpg", aligned)

        return frame