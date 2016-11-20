# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 10:23:16 2016

@author: vs26
"""

import glob
import numpy as np
import os
from scipy.fftpack import dct
from skimage import transform

import cv2
import matplotlib.pyplot as plt

# from __future__ import print_function

plt.close('all')

HAAR_CASCADE_FACE_XML = \
    "C:\\opencv\\sources\\data\\" + \
    "haarcascades_cuda\\haarcascade_frontalface_default.xml"

print (HAAR_CASCADE_FACE_XML)

face_cascade = cv2.CascadeClassifier()
assert face_cascade.load(HAAR_CASCADE_FACE_XML)

# For still image

data_dir = "F:\\DataSet\\"
# img_f = 'C:\\Users\\vs26\\Pictures\\people.jpg' #test image
print (data_dir)

W, H = 100, 100
RETAIN = 8

face_images = []

X_train = []
y_train = []

X_test = []
y_test = []


def dct_2d(a):
    return dct(dct(a.T).T)


# For each person:
# Read jpg files and extract face
# Convert all faces to features - 2d dct
# On first N-1 images build a model
# Test on final image

# get all images from the data set
for i in range(1, 5):
    if i == 9:
        continue

    key = "s{}".format(i)
    print (key)

    s_dir = os.path.join(data_dir, key)

    jpgs = glob.glob("{}\\*.jpg".format(s_dir))

    face_features = []

    for img_f in jpgs:
        if not os.path.exists(img_f):
            print ("Can't find image...")
            continue

        img = cv2.imread(img_f)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #        fig, ax = plt.subplots(1, 2)
        #        ax[0].imshow(img_rgb)
        #        ax[1].imshow(img_grey, cmap=cm.gray)
        #        plt.tight_layout()

        faces = face_cascade.detectMultiScale(img_grey, 1.3, 5, minSize=(200, 200))

        if len(faces) < 1:
            continue

        # Get the face x, y and w, h
        x, y, w, h = faces[0]

        # Extract full size face and resize
        face_img = img_grey[y:y + h, x:x + w]
        face_img = transform.resize(face_img, (W, H))

        # 2d-dct and truncate
        face_dct = dct_2d(face_img)
        face_x = face_dct[:RETAIN, :RETAIN].flatten()
        # face_features is a 64-dimensional feature vector of the face

        # look at zig zag

        face_features.append(face_x)

    print (len(face_features))

    if not len(face_features):
        continue

    test = face_features[-1]
    X_test.append(test)
    y_test.append(i)

    train = face_features[:-1]
    X_train += train
    y_train += [i] * len(train)

y_train = np.array(y_train)
y_test = np.array(y_test)

X_train = np.vstack(X_train)
X_test = np.vstack(X_test)

# print (X_train.shape, y_train.shape)
# print (X_test.shape, y_test.shape)
#
#
# Build model here
# clf = linear_model.LogisticRegression()
# clf.fit(X_train, y_train)
#
# print clf.predict(X_test)
# print y_test
#
# print accuracy_score(clf.predict(X_test), y_test)
#
# with open("face-model-clf.pkl", "wb") as fh:
#     pickle.dump(clf, fh)
# print clf

# logistic_classifier = linear_model.LogisticRegression(C=100.0)
# logistic_classifier.fit(X_train, y_train)
#
# print()
# print("Logistic regression using RBM features:\n%s\n" % (
#    metrics.classification_report(
#        y_test,
#        classifier.predict(X_test))))
#
# print("Logistic regression using raw pixel features:\n%s\n" % (
#    metrics.classification_report(
#        y_test,
#        logistic_classifier.predict(X_test))))

# LogisticRegression
# SVM - SVC

# displays face in greyscale and scaled down

# face_images.append(face_img)
#                            
# plt.figure()
# plt.imshow(face_img, cmap=cm.gray)
#                            
# fig, ax = plt.subplots(1, 1)
# ax.imshow(img_rgb)
# ax.add_patch(
# patches.Rectangle(
# (x, y), w, h, fill=False, edgecolor="red",linewidth=2))
#
#
# ------------------------------ Code 2 ------------------------------

RED = (255, 0, 0)  # For BGR colour space
RED_BGR = (0, 0, 255)

cap = cv2.VideoCapture()
print cap.open(0)

while True:
    ret, img = cap.read()
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(img_grey, 1.2, 3)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), RED_BGR, 2)

    cv2.imshow('Webcam', img)

    k = cv2.waitKey(33)
    if k == 27:
        # Escape
        break

cv2.destroyAllWindows()
cap.release()
