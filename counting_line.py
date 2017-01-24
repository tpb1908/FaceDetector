# -*- coding: utf-8 -*-
"""
Created on Wed Oct 05 12:46:24 2016

@author: johnsona15
"""

# TODO Stop treating tuples like lists


import cv2
import os
import glob
from skimage import transform
from scipy.fftpack import dct
import cPickle as Pickle
import time
import warnings
from FaceCounter import *


def warn(*args, **kwargs):
    pass

warnings.warn = warn


# Colours for drawing on processed frames
DIVIDER_COLOUR = (255, 255, 0)
BOUNDING_BOX_COLOUR = (255, 0, 0)
CENTROID_COLOUR = (0, 0, 255)

# https://github.com/opencv/opencv/tree/master/data/haarcascades
HAAR_CASCADE_FACE_XML = "/haarcascade_frontalface_default.xml"

print os.getcwd() + HAAR_CASCADE_FACE_XML

face_cascade = cv2.CascadeClassifier()
assert face_cascade.load(os.getcwd() + HAAR_CASCADE_FACE_XML)


positions = {}  # For the current frame
old_positions = {}  # To dif against

W, H = 100, 100

retain = 8
with open("face-model-clf2.pkl", "rb") as fh:
    clf, gmm, thresh = Pickle.load(fh)

names = {}

# Loading the people that we have enrolled
for idx, f_dir in enumerate(glob.glob("person_*")):
    names[idx] = f_dir.split("_")[1]


cap = cv2.VideoCapture()


def dct_2d(a):
    return dct(dct(a.T).T)


# Find the centre of a face
def get_centroid(x, y, w, h):
    return x + int(w / 2), y + int(h / 2)


def detect_faces():

    ret, img = cap.read()
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_grey, 1.3, 5)
    # possibly add minSize=(200, 200)
    matches = []
    global old_positions
    old_positions = positions.copy()  # Copy previous values
    for (x, y, w, h) in faces:
        centroid = get_centroid(x, y, w, h)  # Find the central position

        face_img = img_grey[y:y + h, x:x + w]  # Convert the image to grey-scale
        face_img = transform.resize(face_img, (w, h))

        # 2d-dct and truncate
        face_dct = dct_2d(face_img)
        face_x = face_dct[:retain, :retain].flatten().reshape((1, -1))

        # Check if we recognise the face
        impostor = gmm.score(face_x) < thresh

        if not impostor:
            pred_cls = clf.predict(face_x)[0]
            pred_name = names[pred_cls]

            if pred_name in positions:
                positions[pred_name] = (centroid, int(time.time()), positions[pred_name][2])
            else:
                positions[pred_name] = (centroid, int(time.time()), 0)

        else:
            # FIXME We only add impostors to make it easier to test
            pred_name = "Impostor"
            if pred_name in positions:
                positions[pred_name] = (centroid, int(time.time()), positions[pred_name][2])
            else:
                positions[pred_name] = (centroid, int(time.time()), 0)  # A new person

        matches.append((pred_name, (x, y, w, h), centroid))

    return matches


def process_frame(frame, face_counter):

    # Draw the boundary line
    # TODO Make the position optional so that we can detect line crossing anywhere, or multiple lines
    cv2.line(frame, (0, face_counter.divider), (frame.shape[1], face_counter.divider), DIVIDER_COLOUR, 1)

    matches = detect_faces()
    for (i, match) in enumerate(matches):
        name, face, centroid = match

        x, y, w, h = face

        # Mark the bounding box and the centroid on the processed frame
        cv2.rectangle(frame, (x, y), (x + w - 1, y + h - 1), BOUNDING_BOX_COLOUR, 1)
        cv2.circle(frame, centroid, 2, CENTROID_COLOUR, -1)

        if name in positions:
            cv2.putText(
                frame, "{} {}".format(name, positions[name][2]), (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)
        else:  # If the person is new
            cv2.putText(
                frame, "{}".format(name), (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)

    face_counter.update_count(matches, frame)

    for (n1, t1), (n2, t2) in zip(positions.items(), old_positions.items()):
        if (t1[0][1] > H / 2 > t2[0][1]) or (t1[0][1] < H / 2 < t2[0][1]):
            print("{} crossed the line at {}".format(n1, t1[1]))
            # TODO Don't do this
            positions[n1] = (positions[n1][0], positions[n1][1], positions[n1][2] + 1)

    # We search for people that we haven't detected for 3 seconds
    for (n, c) in positions.items():
        if c[1] + 3 < int(time.time()):
            del positions[n]
    return frame


def main():
    face_counter = None  # Will be created after first frame is captured
    # Set up image source
    assert cap.open(0)

    global W, H

    while cap.isOpened():
        ret, frame = cap.read()
        W, H = tuple(frame.shape[1::-1])  # Get the width and height of the frame
        # print("H {} W {}".format(H, W))
        if not ret:
            print("Error")
            break

        if face_counter is None:
            # We do this here, so that we can initialize with actual frame size
            face_counter = FaceCounter(frame.shape[:2], frame.shape[0] / 2)

        cv2.imshow('Processed Image', process_frame(frame, face_counter))

        k = cv2.waitKey(33)
        if k != -1:
            # Escape
            cap.release()

    # Apparently CV2 windows are a bit shit, and so we have to try waitKey a few times for the window to close
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    for i in range(1, 5):
        cv2.waitKey(1)


main()
