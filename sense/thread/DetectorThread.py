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
            if not self._alive:
                return
            if self._next is not None:
                self._thread_lock.acquire()
                
                frame = self._next
                self.process_faces(frame)
                self.process_eyes(frame)
                
                self._thread_lock.release()

            time.sleep(0.005)
            # print("Is main thread? " + str(isinstance(threading.currentThread(), threading._MainThread)))
                
    def kill(self):
        self._thread_lock.acquire()
        self._alive = False
        print "Stopping thread"
        self._thread_lock.release()

    def dispose(self):
        self.kill()

    def update_frame(self, frame):
        self._next = frame.copy()
        
    def set_detector(self, detector):
        self._detection = detector
        
    def process_faces(self, frame):
        live_people = {}
        people = self._people.copy()
        
        i = 0
        for face in self._detection.get_faces(frame):
            i += 1
            is_imposter = self.gmm.score(face.features()) < self.thresh

            # Get the name of the face
            name = "Imposter" + str(i)
            if not is_imposter:
                prediction = self.clf.predict(face.features())[0]
                name = self._names[prediction]

            # Update/create the person
            if name in self._people:
                people[name].update(face)
            else:
                people[name] = Person(face, name)

            live_people[name] = people[name]

        print ("Live people: ", len(live_people))

        # Remove inactive people
        for (name, person) in people.items():
            if not person.active():
                del people[name]
        self._people = people
        self._live_people = live_people
        
    def process_eyes(self, frame):
        eyes = self._detection.get_eyes(frame)
        self._eyes = eyes
        
    def live_people(self):
        return self._live_people

    def active_people(self):
        return self._people

    def get_eyes(self):
        return self._eyes
