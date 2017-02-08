import threading
import time
import cPickle as Pickle
import glob

from sense.Person import Person


class DetectorThread(threading.Thread):

    def __init__(self, detector):
        threading.Thread.__init__(self)

        self._thread_lock = threading.Lock()
        self._detection = detector
        self._next = None

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
        self._alive = True

    def run(self):
        while True:
            if self._next is not None:
                self.process_faces(self._next)
                self.process_eyes(self._next)
            time.sleep(0.005)
            if not self._alive:
                return
                
    def kill(self):
        self._thread_lock.acquire()
        self._alive = False
        print "Stopping thread"
        self._thread_lock.release()

    def update_frame(self, item):
        self._thread_lock.acquire()
        self._next = item
        self._thread_lock.release()

    def set_detector(self, detector):
        self._thread_lock.acquire()
        self._detection = detector
        self._thread_lock.release()

    def process_faces(self, frame):
        live_people = {}
        people = self._people.copy()
        for face in self._detection.get_faces(frame):
            is_imposter = self.gmm.score(face.features()) < self.thresh

            # Get the name of the face
            name = "Imposter"
            if not is_imposter:
                prediction = self.clf.predict(face.features())[0]
                name = self._names[prediction]

            # Update/create the person
            if name in self._people:
                people[name].update(face)
            else:
                people[name] = Person(face, name)

            live_people[name] = people[name]

        # Remove inactive people
        for (name, person) in people.items():
            if not person.active():
                del people[name]
        self._thread_lock.acquire()
        self._people = people
        self._live_people = live_people
        self._thread_lock.release()

    def process_eyes(self, frame):
        eyes = self._detection.get_eyes(frame)
        self._thread_lock.acquire()
        self._eyes = eyes
        self._thread_lock.release()

    def live_people(self):
        return self._live_people

    def active_people(self):
        return self._people

    def get_eyes(self):
        return self._eyes
