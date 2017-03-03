import cPickle as Pickle
import glob

from sense.Person import Person
import sense.recognition.Cv2Recognition as recog

class Cv2Recognition(object):
    def __init__(self, detection):
        self._detection = detection

        # Map of names to active people
        self._people = {}
        # Map of names to people in the last frame
        self._live_people = {}

        self._recog = recog()

        self._eyes = []

    def set_detection(self, detection):
        self._detection = detection

    def update_frame(self, frame):
        self.process_faces(frame)
        self.process_eyes(frame)

    def kill(self):
        pass

    def start(self):
        pass

    def dispose(self):
        pass

    def process_faces(self, frame):
        self._live_people = {}
        
        i = 0
        for face in self._detection.get_faces(frame):
            i += 1
            name = self._recog.get_name(face)
            if name == "IMPOSTER":
                name = name + str(i)

            # Update/create the person
            if name in self._people:
                self._people[name].update(face)
            else:
                self._people[name] = Person(face, name)

            self._live_people[name] = self._people[name]

        # Remove inactive people
        for (name, person) in self._people.items():
            if not person.active():
                del self._people[name]

    def process_eyes(self, frame):
        self._eyes = self._detection.get_eyes(frame)

    def live_people(self):
        return self._live_people

    def people(self):
        return self._people

    def get_eyes(self):
        return self._eyes

