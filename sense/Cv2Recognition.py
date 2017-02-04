import cPickle as Pickle
import glob

from sense.Person import Person


class Cv2Recognition(object):
    def __init__(self, detector):
        self._detection = detector

        # Map of names to active people
        self._people = {}
        # Map of names to people in the last frame
        self._live_people = {}

        # Loading the people that we have enrolled
        self._names = {}
        for idx, f_dir in enumerate(glob.glob("person_*")):
            self._names[idx] = f_dir.split("_")[1]

        # Load face model
        with open("data/face-model.pkl", "rb") as fh:
            self.clf, self.gmm, self.thresh = Pickle.load(fh)

        self._eyes = []

    def set_detector(self, detector):
        self._detection = detector

    def process_faces(self, frame):
        self._live_people = {}
        for face in self._detection.get_faces(frame):
            is_imposter = self.gmm.score(face.features()) < self.thresh

            # Get the name of the face
            name = "Imposter"
            if not is_imposter:
                prediction = self.clf.predict(face.features())[0]
                name = self._names[prediction]

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

    def active_people(self):
        return self._people

    def get_eyes(self):
        return self._eyes

