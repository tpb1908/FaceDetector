from sense.recognition.Recognition import Recognition

import openface

import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder

import os
import pandas as pd
import cPickle as pickle
import cv2

from operator import itemgetter

class OpenfaceRecognition(Recognition):
    CLASSIFIER = os.path.join(os.getcwd(), "people-embeddings/classifier.pkl")
    
    def __init__(self):
        super(OpenfaceRecognition, self).__init__()
        self.net = openface.TorchNeuralNet("/home/amber/openface/models/openface/nn4.small2.v1.t7", imgDim=96, cuda=False)
        self.clf = SVC(C=1, kernel='linear', probability=True)
        
        fname = os.path.join(os.getcwd(), "people-embeddings/labels.csv")
        print fname
        labels = pd.read_csv(fname, header=None).as_matrix()[:, 1]
        labels = map(itemgetter(1),
                    map(os.path.split,
                        map(os.path.dirname, labels)))
        self.le = LabelEncoder().fit(labels)

    def getRep(self, face):
        return self.net.forward(face)
        
    def get_name(self, face):
        with open(OpenfaceRecognition.CLASSIFIER, 'r') as f:
            (le, clf) = pickle.load(f)

        # image = cv2.cvtColor(face.frameface(), cv2.COLOR_BGR2RGB)
        r = self.getRep(face.frameface())
        rep = r[1].reshape(1, -1)
        bbx = r[0]
        
        predictions = self.clf.predict_proba(rep).ravel()
        maxI = np.argmax(predictions)

        person = le.inverse_transform(maxI)
        confidence = predictions[maxI]

        print "Predicted: {}, with cofidence: {}".format(person, confidence)
        return person