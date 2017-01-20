# -*- coding: utf-8 -*-
"""
Created on Wed Oct 05 12:46:24 2016

@author: johnsona15
"""


import cv2
import matplotlib.pyplot as plt
import os
import glob
from skimage import transform
from scipy.fftpack import dct
import cPickle as Pickle
import time

from FaceCounter import *


def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

plt.close('all')


LOG_TO_FILE = True

# Colours for drawing on processed frames
DIVIDER_COLOUR = (255, 255, 0)
BOUNDING_BOX_COLOUR = (255, 0, 0)
CENTROID_COLOUR = (0, 0, 255)

# https://github.com/opencv/opencv/tree/master/data/haarcascades
HAAR_CASCADE_FACE_XML = "/haarcascade_frontalface_default.xml"

print os.getcwd() + HAAR_CASCADE_FACE_XML

face_cascade = cv2.CascadeClassifier()
assert face_cascade.load(os.getcwd() + HAAR_CASCADE_FACE_XML)

RED = (255, 0, 0)
RED_BGR = (0, 0, 255)


positions = {}
old_positions = {}

W, H = 100, 100

retain = 8
with open("face-model-clf2.pkl", "rb") as fh:
    clf, gmm, thresh = Pickle.load(fh)

names = {}

# Finding people
for idx, f_dir in enumerate(glob.glob("person_*")):
    names[idx] = f_dir.split("_")[1]

# Getting the cluster of points (?)


def get_centroid(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)

    cx = x + x1
    cy = y + y1

    return cx, cy


cap = cv2.VideoCapture()
print cap.open(0)


def dct_2d(a):
    return dct(dct(a.T).T)


def detect_faces():
    # ctr = 0

    ret, img = cap.read()
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_grey, 1.3, 5)
    # possibly add minSize=(200, 200)
    matches = []
    global old_positions
    old_positions = positions.copy()  # Copy previous values
    for (x, y, w, h) in faces:
        # cv2.rectangle(img, (x, y), (x + w, y + h), RED_BGR, 2)  # Draw a rectangle around the match
        centroid = get_centroid(x, y, w, h)  # Find the central position

        face_img = img_grey[y:y + h, x:x + w]  # Convert the image to grey-scale
        face_img = transform.resize(face_img, (w, h))

        # 2d-dct and truncate
        face_dct = dct_2d(face_img)
        face_x = face_dct[:retain, :retain].flatten().reshape((1, -1))

        impostor = gmm.score(face_x) < thresh

        if not impostor:
            pred_cls = clf.predict(face_x)[0]
            pred_name = names[pred_cls]

            if pred_name in positions:
                positions[pred_name] = (centroid, int(time.time()))
            else:
                positions[pred_name] = (centroid, int(time.time()))

        else:
            # TODO Don't add impostors to positions
            pred_name = "Impostor"
            if pred_name in positions:
                # print("Updating persons position")
                positions[pred_name] = (centroid, int(time.time()))
            else:
                # print("Adding person to positions")
                positions[pred_name] = (centroid, int(time.time()))

        matches.append((pred_name, (x, y, w, h), centroid))
    # We don't really need to show the person their face twice
    # cv2.imshow('Webcam', img)

    return matches


def save_frame(file_name_format, frame_number, frame):
    file_name = file_name_format % frame_number

    cv2.imwrite(file_name, frame)


def process_frame(frame, face_counter):  # , img

    # Create a copy of source frame to draw into
    processed = frame.copy()

    # Draw dividing line -- we count things as they cross this line.
    cv2.line(processed, (0, face_counter.divider), (frame.shape[1], face_counter.divider), DIVIDER_COLOUR, 1)

    # save_frame("/mask_%04d.png"
    #   , frame_number, frame, "foreground mask for frame #%d")
    matches = detect_faces()
    for (i, match) in enumerate(matches):
        name, face, centroid = match

        x, y, w, h = face

        # Mark the bounding box and the centroid on the processed frame
        cv2.rectangle(processed, (x, y), (x + w - 1, y + h - 1), BOUNDING_BOX_COLOUR, 1)
        cv2.circle(processed, centroid, 2, CENTROID_COLOUR, -1)

        cv2.putText(
            processed, "{}".format(name), (x, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)

    face_counter.update_count(matches, processed)

    # print("Positions {} Old positions {}".format(str(len(positions)), str(len(old_positions))))
    for (n1, c1), (n2, c2) in zip(positions.items(), old_positions.items()):
        # print("{} at {} from {}".format(n1, c1, c2))

        if (c1[0][1] > H / 2 > c2[0][1]) or (c1[0][1] < H / 2 < c2[0][1]):
            print("{} crossed the line at {}".format(n1, c1[1]))
            pass
            # Found someone crossing the line
    for (n, c) in positions.items():
        if c[1] + 3 < int(time.time()):
            del positions[n]
    return processed


def main():
    face_counter = None  # Will be created after first frame is captured
    # Set up image source
    ctr = 0
    cap.open(0)
    print(cap.isOpened())
    frame_number = -1

    global W, H

    while True:
        frame_number += 1
        ret, frame = cap.read()
        W, H = tuple(frame.shape[1::-1]) # Get the width and height of the frame
        # print("H {} W {}".format(H, W))
        if not ret:
            print("Error")
            break

        if face_counter is None:
            # We do this here, so that we can initialize with actual frame size
            face_counter = FaceCounter(frame.shape[:2], frame.shape[0] / 2)

        processed = process_frame(frame, face_counter)

        cv2.imshow('Processed Image', processed)

        k = cv2.waitKey(33)
        if k != -1:
            # Escape
            cap.release()

        ctr += 1

    # Apparently CV2 windows are a bit shit, and so we have to try waitKey a few times for the window to close
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    for i in range(1, 5):
        cv2.waitKey(1)


main()
