# -*- coding: utf-8 -*-
"""
Created on Mon Aug 08 11:29:22 2016

@author: vs26
"""

import cv2
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import patches
import numpy as np
import os
from sklearn.feature_extraction import image
import glob
from skimage import transform
from scipy.fftpack import dct
from sklearn.metrics import accuracy_score
import cPickle as pickle
from skimage.io import imsave
from sklearn.decomposition import PCA


#FIXME Ignoring warnings
# Some method being called is deprecated
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

plt.close('all')

HAAR_CASCADE_FACE_XML = "/haarcascade_frontalface_default.xml"

print (HAAR_CASCADE_FACE_XML)

face_cascade = cv2.CascadeClassifier()
assert (face_cascade.load(os.getcwd() + HAAR_CASCADE_FACE_XML))

with open("face-model-clf2-new.pkl", "rb") as fh:
    clf, gmm, thresh = pickle.load(fh)
# print clf


RED = (255, 0, 0)  # For BGR colour space
RED_BGR = (0, 0, 255)

cap = cv2.VideoCapture()
print cap.open(0)


def dct_2d(a):
    return dct(dct(a.T).T)


RETAIN = 8
W, H = 100, 100

ctr = 0
names = {}

for idx, f_dir in enumerate(glob.glob("person_*")):
    names[idx] = f_dir.split("_")[1]

while True:
    ret, img = cap.read()
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(img_grey, 1.2, 5, minSize=(150, 150))

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), RED_BGR, 2)

        face_img = img_grey[y:y + h, x:x + w]
        face_img = transform.resize(face_img, (W, H))

        # imsave(os.path.join("Amber", "{}_.png".format(ctr)), face_img)

        # 2d-dct and truncate
        face_dct = dct_2d(face_img)
        face_x = face_dct[:RETAIN, :RETAIN].flatten().reshape((1, -1))

        imposter = gmm.score(face_x) < thresh

        #        face_x = face_img.flatten().reshape((1, -1))
        #        face_x = pca.transform(face_x)

        if not imposter:
            # print clf.predict(face_x)
            pred_cls = clf.predict(face_x)[0]
            pred_name = names[pred_cls]
        else:
            pred_name = "Imposter"

        cv2.putText(
            img, "{}".format(pred_name), (x, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)

    cv2.imshow('Webcam', img)

    k = cv2.waitKey(33)
    if k != -1:
        # Escape
        break

    ctr += 1

cv2.destroyAllWindows()
cap.release()
