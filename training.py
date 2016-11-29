# -*- coding: utf-8 -*-
"""
Created on Mon Aug 08 14:24:57 2016

@author: vs26
"""
import warnings
import cv2
import numpy as np
import os
import glob
from scipy.fftpack import dct
from sklearn.metrics import accuracy_score
from sklearn import linear_model
from sklearn.mixture import GMM
import cPickle as Pickle


# FIXME Ignoring warnings
# Some method being called is deprecated


def train():

    w, h = 100, 100
    retain = 8

    face_images = []

    x_train = []
    y_train = []

    x_test = []
    y_test = []

    def dct_2d(a):
        return dct(dct(a.T).T)

    # Get all images from the data set
    for i, el in enumerate(glob.glob("person_*")):
        print el, i

        key = el
        print (key)

        pngs = glob.glob("{}/*.png".format(key))
        face_features = []

        for img_f in pngs:
            if not os.path.exists(img_f):
                print ("Can't find images...")
                continue

            face_img = cv2.imread(img_f, 0)

            # 2d-dct and truncate
            face_dct = dct_2d(face_img)
            face_x = face_dct[:retain, :retain].flatten()

            # face_features is a 64-dimensional feature vector of the face

            # look at zig zag

            face_features.append(face_x)

        print len(face_features)

        if not len(face_features):
            continue

        test = face_features[-10:]
        x_test.append(test)
        y_test += [i] * len(test)

        train = face_features[:-10]
        x_train += train
        y_train += [i] * len(train)

    y_train = np.array(y_train)
    y_test = np.array(y_test)

    x_train = np.vstack(x_train)
    x_test = np.vstack(x_test)

    print (x_train.shape, y_train.shape)
    print (x_test.shape, y_test.shape)

    gmm = GMM(n_components=8)
    gmm.fit(x_train)

    thresh = np.percentile(gmm.score(x_test), 5)

    # Build model here
    clf2 = linear_model.LogisticRegression()
    clf2.fit(x_train, y_train)

    print "Subject number given to the algorithm: "
    print clf2.predict(x_test)
    print "Subject number predicted by the algorithm: "
    print y_test

    print "Accuracy score:"
    print accuracy_score(clf2.predict(x_test), y_test)

    with open("face-model-clf2.pkl", "wb") as fh:
        Pickle.dump([clf2, gmm, thresh], fh)
