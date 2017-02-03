import glob
import cv2
import os
import cPickle as Pickle

from Filter import Filter
from Face import Face
from Person import Person


class CountingLine(Filter):
    # Source: https://github.com/opencv/opencv/tree/master/data/haarcascades
    HAAR_CASCADE_FACE_XML = "/cascades/haarcascade_frontalface_default.xml"

    # Colours for drawing on processed frames
    DIVIDER_COLOUR = (255, 255, 0)
    BOUNDING_BOX_COLOUR = (255, 0, 0)
    CENTROID_COLOUR = (0, 0, 255)

    def __init__(self, width, height):
        super(CountingLine, self).__init__(width, height)

        self.people = {}

        # Loading the people that we have enrolled
        self.names = {}
        for idx, f_dir in enumerate(glob.glob("person_*")):
            self.names[idx] = f_dir.split("_")[1]

        # Load cascade
        self.face_cascade = cv2.CascadeClassifier()
        print(str(os.getcwd() + CountingLine.HAAR_CASCADE_FACE_XML))
        assert self.face_cascade.load(os.getcwd() + CountingLine.HAAR_CASCADE_FACE_XML)
        
        # Load face model
        with open("face-model.pkl", "rb") as fh:
            self.clf, self.gmm, self.thresh = Pickle.load(fh)

    def apply(self, frame):
        # Draw the boundary line
        # TODO Make the position optional so that we can detect line crossing anywhere, or multiple lines
        filter = super(CountingLine, self)

        matches = self.detect_faces(frame)

        cv2.line(frame, (0, filter.height() / 2), (filter.width(), filter.height() / 2),
                     CountingLine.DIVIDER_COLOUR, 1)

        for person in matches:
            shape = person.shape()

            # Mark the bounding box and the centroid on the processed frame
            cv2.rectangle(frame,
                          (shape.x, shape.y),
                          (shape.x + shape.width - 1, shape.y + shape.height - 1),
                          CountingLine.BOUNDING_BOX_COLOUR,
                          1)
            cv2.circle(frame, person.centroid(), 2, CountingLine.CENTROID_COLOUR, -1)

            name = person.name()
            if name in self.people:
                cv2.putText(
                    frame, "{} {}".format(name, self.people[name].count()), (shape.x, shape.y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)
            else:
                # Person is new
                cv2.putText(
                    frame, "{}".format(name), (shape.x, shape.y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)

        # Check if person has crossed the line
        for (name, person) in self.people.items():
            if person.has_crossed(super(CountingLine, self).height() / 2):
                print("{} crossed the line".format(name))
                person.increment()

        # Remove people that we haven't detected for 3 seconds
        for (name, person) in self.people.items():
            if not person.active():
                print("Deleting " + name)
                del self.people[name]
        
        return frame
        
    def detect_faces(self, frame):
        # Detect face positions in frame
        img_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # possibly add minSize=(200, 200)
        faces = self.face_cascade.detectMultiScale(img_grey, 1.3, 5)
        
        matches = []
        for position in faces:
            face = Face(position, img_grey)
            
            # Check if we recognise the face
            impostor = self.gmm.score(face.features()) < self.thresh

            # Get the name of the face
            pred_name = "Impostor"
            if not impostor:
                pred_cls = self.clf.predict(face.features())[0]
                pred_name = self.names[pred_cls]

            # Update (or create) the person
            if pred_name in self.people:
                self.people[pred_name].update(face)
            else:
                self.people[pred_name] = Person(face, pred_name)

            # Add them to the list of matches
            matches.append(self.people[pred_name])

        return matches
