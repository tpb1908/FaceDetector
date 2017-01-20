# -*- coding: utf-8 -*-
"""
Created on Mon Aug 08 11:44:19 2016

@author: vs26
"""
import cv2
import matplotlib.pyplot as plt
import os
from skimage import transform
from scipy.fftpack import dct
from skimage.io import imsave
import training


plt.close('all')

HAAR_CASCADE_FACE_XML = "/haarcascade_frontalface_default.xml"

face_cascade = cv2.CascadeClassifier()
assert (face_cascade.load(os.getcwd() + HAAR_CASCADE_FACE_XML))

RED = (255, 0, 0)
RED_BGR = (0, 0, 255)

face_features = []
X_train = []
y_train = []

X_test = []
y_test = []
names = []


def dct_2d(a):
    return dct(dct(a.T).T)


def begin_enrolment():
    # Ask for name
    name = raw_input("What is your name? ")
    name = "person_{}".format(name)

    # for idx, folder in enumerate(glob.glob('person_*')):
    #    name = folder.split('_')[1]
    #    names[idx] = name

    # Create folder for new person
    if not os.path.exists(name):
        os.makedirs(name)

    # Collect and save images using cv2
    retain = 8
    w, h = 100, 100

    cap = cv2.VideoCapture()
    print "Camera open " + str(cap.open(0))

    path, dirs, files = os.walk(name).next()
    ctr = len(files)

    while cap.isOpened():
        ret, img = cap.read()
        img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(img_grey, 1.3, 5)
        # Possibly add minSize=(200, 200)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), RED_BGR, 2)
            face_img = img_grey[y:y + h, x:x + w]
            face_img = transform.resize(face_img, (w, h))
            imsave(os.path.join(name, "{}_.png".format(ctr)), face_img)
            cv2.putText(
                img, "{}".format(ctr), (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)

        cv2.imshow('Webcam', img)

        k = cv2.waitKey(33)
        if k != -1:
            cap.release()

        ctr += 1

    # Apparently CV2 windows are a bit shit, and so we have to try waitKey a few times for the window to close
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    for i in range(1, 5):
        cv2.waitKey(1)

    print 'Capture complete, beginning training'
    training.train()

