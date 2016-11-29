# -*- coding: utf-8 -*-
"""
Created on Mon Aug 08 11:29:22 2016

@author: vs26
"""

import warnings
import cv2
import matplotlib.pyplot as plt
import os
import glob
from skimage import transform
from scipy.fftpack import dct
import cPickle as Pickle


plt.close('all')

HAAR_CASCADE_FACE_XML = "/haarcascade_frontalface_default.xml"

print (HAAR_CASCADE_FACE_XML)

face_cascade = cv2.CascadeClassifier()
assert (face_cascade.load(os.getcwd() + HAAR_CASCADE_FACE_XML))


def test():
    with open("face-model-clf2.pkl", "rb") as fh:
        clf, gmm, thresh = Pickle.load(fh)

    r_e_d = (255, 0, 0)  # For BGR colour space
    r_e_d__b_g_r = (0, 0, 255)

    cap = cv2.VideoCapture()
    print "Opening camera " + str(cap.open(0))

    def dct_2d(a):
        return dct(dct(a.T).T)

    retain = 8
    w, h = 100, 100

    ctr = 0
    names = {}

    # Finding people
    for idx, f_dir in enumerate(glob.glob("person_*")):
        names[idx] = f_dir.split("_")[1]

    while True:
        ret, img = cap.read()
        img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(img_grey, 1.2, 5, minSize=(150, 150))

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), r_e_d__b_g_r, 2)

            face_img = img_grey[y:y + h, x:x + w]
            face_img = transform.resize(face_img, (w, h))

            # 2d-dct and truncate
            face_dct = dct_2d(face_img)
            face_x = face_dct[:retain, :retain].flatten().reshape((1, -1))

            impostor = gmm.score(face_x) < thresh

            if not impostor:
                pred_cls = clf.predict(face_x)[0]
                pred_name = names[pred_cls]
            else:
                pred_name = "Impostor"

            cv2.putText(
                img, "{}".format(pred_name), (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)

        cv2.imshow('Webcam', img)

        k = cv2.waitKey(33)
        if k != -1:  # Any key press
            # Escape
            break

        ctr += 1

    cv2.destroyAllWindows()
    cap.release()
