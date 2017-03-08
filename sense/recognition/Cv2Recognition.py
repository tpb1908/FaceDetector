import cPickle as Pickle
import glob

from sense.recognition.Recognition import Recognition


class Cv2Recognition(Recognition):
    def __init__(self):
        super(Cv2Recognition, self).__init__()

        # Load enrolled people
        self._names = {}
        for i, folder in enumerate(glob.glob("person_*")):
            self._names[i] = folder.split("_")[1]

        # Load face model
        with open("data/face-model.pkl", "rb") as fh:
            self._clf, self._gmm, self._thresh = Pickle.load(fh)

    def get_name(self, face):
        is_imposter = self._gmm.score(face.features()) < self._thresh
        if not is_imposter:
            prediction = self._clf.predict(face.features())[0]
            return self._names[prediction]

        return "IMPOSTER"
