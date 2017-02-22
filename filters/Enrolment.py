import os
import cv2
from skimage.io import imsave

from filters.Filter import Filter


class Enrolment(Filter):

    NAME = "Enrolment"

    def __init__(self, width, height, sense, active=False):
        super(Enrolment, self).__init__(width, height, Enrolment.NAME, sense, active)

        self._images = []
        self.name = None
        self.name = "Test name"
        self.ctr = 0
        self.start()

    def start(self):  # Start recording features
        # self.name = raw_input("What is your name? ")
        self.name = "person_{}".format(self.name)
        self._images = []
        if not os.path.exists(self.name):
            os.makedirs(self.name)
        path, dirs, files = os.walk(self.name).next()
        self.ctr = len(files)
        print "Starting with " + str(self.ctr)

    def done(self):  # Complete the recording of a person
        pass

    def process_frame(self, frame):
        if self.name is None:  # If we aren't recording
            return frame

        people = self._sense.live_people()
        if len(people) > 1 or len(people) == 0:  # We can only deal with one person
            print "Can't enrol " + str(len(people))
        else:
            person = people.itervalues().next()
            self._images.append(person.face().image())
            shape = person.shape()
            cv2.putText(
                frame, "{}/{}".format(len(self._images), self.ctr),
                (shape.x + shape.width, shape.y + shape.height),
                cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)
            imsave(os.path.join(self.name, "{}_.png".format(self.ctr)), self._images[-1])
            self.ctr += 1
            
        return frame
