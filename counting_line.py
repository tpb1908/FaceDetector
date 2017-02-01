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

from Face import Face
from Person import Person

DEBUG = False

# Disable deprecation warning
def warn(*args, **kwargs):
    pass
if not DEBUG:
    warnings.warn = warn

# Colours for drawing on processed frames
DIVIDER_COLOUR = (255, 255, 0)
BOUNDING_BOX_COLOUR = (255, 0, 0)
CENTROID_COLOUR = (0, 0, 255)

# https://github.com/opencv/opencv/tree/master/data/haarcascades
HAAR_CASCADE_FACE_XML = "/haarcascade_frontalface_default.xml"

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

def detect_faces():
    ret, img = cap.read()
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_grey, 1.3, 5)
    # possibly add minSize=(200, 200)
    matches = []
    global old_positions
    old_positions = positions.copy()  # Copy previous values
    for position in faces:
        face = Face(position, img_grey)
        
        # Check if we recognise the face
        impostor = gmm.score(face.features()) < thresh

        if not impostor:
            pred_cls = clf.predict(face_x)[0]
            pred_name = names[pred_cls]

            if pred_name in positions:
                positions[pred_name].update(face)
            else:
                positions[pred_name] = Person(face, pred_name)

        else:
            # FIXME We only add impostors to make it easier to test
            pred_name = "Impostor"
            if pred_name in positions:
                positions[pred_name].update(face)
            else:
                positions[pred_name] = Person(face, pred_name)

        matches.append((pred_name, face))

    return matches


def process_frame(frame, face_counter):
    # Draw the boundary line
    # TODO Make the position optional so that we can detect line crossing anywhere, or multiple lines
    cv2.line(frame, (0, face_counter.divider), (frame.shape[1], face_counter.divider), DIVIDER_COLOUR, 1)

    matches = detect_faces()
    for (i, match) in enumerate(matches):
        name, face = match
        shape = face.shape()

        # Mark the bounding box and the centroid on the processed frame
        cv2.rectangle(frame, (shape.x, shape.y), (shape.x + shape.width - 1, shape.y + shape.height - 1), BOUNDING_BOX_COLOUR, 1)
        cv2.circle(frame, face.centroid(), 2, CENTROID_COLOUR, -1)

        if name in positions:
            cv2.putText(
                frame, "{} {}".format(name, positions[name].shape().y), (shape.x, shape.y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)
        else:
            # Person is new
            cv2.putText(
                frame, "{}".format(name), (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)

    face_counter.update_count(matches, frame)

    for (n1, person), (n2, old_person) in zip(positions.items(), old_positions.items()):
        # Check is person has crossed the line
        if person.has_crossed(H / 2):
            print("{} crossed the line".format(n1))
            person.count()

    # We search for people that we haven't detected for 3 seconds
    for (n, person) in positions.items():
        if not person.active():
            print("deleting")
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

        processed_frame = process_frame(frame, face_counter)
        cv2.imshow('Processed Image', processed_frame)

        k = cv2.waitKey(33)
        # TODO: Sort key input out 
        # Escape
        if k == 27:
            cap.release()

    # Apparently CV2 windows are a bit shit, and so we have to try waitKey a few times for the window to close
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    for i in range(1, 5):
        cv2.waitKey(1)


main()
