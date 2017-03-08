from sense.Person import Person

from sense.detection.DlibDetection import DlibDetection
from sense.recognition.Cv2Recognition import Cv2Recognition


class Sense(object):
    def __init__(self, detection=DlibDetection(), recogniton=Cv2Recognition()):
        self._detection = detection
        self._recognition = recogniton

        # TODO: can we remove this?
        self._people = {}  # People that have been in a frame recently
        self._active_people = {}  # People in the latest frame

        self._eyes = []

    def set_detection(self, detection):
        self._detection = detection

    def set_recognition(self, recognition):
        self._recognition = recognition

    def process_frame(self, frame):
        self._active_people = {}

        # TODO: merge this with person 
        # TODO: use face image to speed up eye detection
        self._eyes = self._detection.get_eyes(frame)

        i = 0
        for face in self._detection.get_faces(frame):
            name = self._recognition.get_name(face)
            # TODO: instead of updating people by name, update people by id.
            if name == "IMPOSTER":
                name += str(i)
                i += 1

            # Update/create the person
            if name in self._people:
                self._people[name].update(face)
            else:
                self._people[name] = Person(face, name)
            self._active_people[name] = self._people[name]

        # Remove inactive people
        for (name, person) in self._people.items():
            if not person.active():
                del self._people[name]

    def people(self):
        return self._people

    def active_people(self):
        return self._active_people

    # TODO: merge with person
    def eyes(self):
        return self._eyes
