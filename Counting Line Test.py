# -*- coding: utf-8 -*-
"""
Created on Wed Oct 05 12:46:24 2016

@author: johnsona15
"""

import cv2
import matplotlib.pyplot as plt
import os
from skimage import transform
from scipy.fftpack import dct
from skimage.io import imsave
import glob
import logging
import logging.handlers
import time
import sys
import numpy as np

from FaceCounter import *

plt.close('all')

# Time to wait between frames, 0=forever
WAIT_TIME = 1  # 250 # ms

LOG_TO_FILE = True

# Colours for drawing on processed frames    
DIVIDER_COLOUR = (255, 255, 0)
BOUNDING_BOX_COLOUR = (255, 0, 0)
CENTROID_COLOUR = (0, 0, 255)

#https://github.com/opencv/opencv/tree/master/data/haarcascades
HAAR_CASCADE_FACE_XML = "/haarcascade_frontalface_default.xml"

print os.getcwd() + HAAR_CASCADE_FACE_XML

face_cascade = cv2.CascadeClassifier()
assert (face_cascade.load(os.getcwd() + HAAR_CASCADE_FACE_XML))

RED = (255, 0, 0)
RED_BGR = (0, 0, 255)

W, H = 100, 100


# getting the cluster of points (?)
def get_centroid(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)

    cx = x + x1
    cy = y + y1

    return (cx, cy)


cap = cv2.VideoCapture()
# print ("Hello")
print cap.open(0)

# faces is contour_valid, matches is matches
ctr = 0


def detect_Faces(img):
    # ctr = 0
    i = 0
    while True:
        i += 1
        ret, img = cap.read()
        img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(img_grey, 1.3, 5)
        # possibly add minSize=(200, 200) 
        matches = []
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), RED_BGR, 2)
            centroid = get_centroid(x, y, w, h)

            matches.append(((x, y, w, h), centroid))

        cv2.imshow('Webcam', img)

        print(len(matches))
        if (len(matches) >= 1):
            break

    return matches


def save_frame(file_name_format, frame_number, frame, label_format):
    file_name = file_name_format % frame_number

    cv2.imwrite(file_name, frame)


def process_frame(frame_number, frame, face_counter):  # , img

    # Create a copy of source frame to draw into
    processed = frame.copy()

    # Draw dividing line -- we count cars as they cross this line.
    cv2.line(processed, (0, face_counter.divider), (frame.shape[1], face_counter.divider), DIVIDER_COLOUR, 1)
    print("Doing something- line")

    # save_frame("/mask_%04d.png"
    #   , frame_number, frame, "foreground mask for frame #%d")
    # print("Doing something - saved")
    matches = detect_Faces(frame)
    print("Doing something- found faces")
    for (i, match) in enumerate(matches):
        face, centroid = match

        x, y, w, h = face

        # Mark the bounding box and the centroid on the processed frame
        # NB: Fixed the off-by one in the bottom right corner
        cv2.rectangle(processed, (x, y), (x + w - 1, y + h - 1), BOUNDING_BOX_COLOUR, 1)
        cv2.circle(processed, centroid, 2, CENTROID_COLOUR, -1)
    print("Doing something - loop")
    face_counter.update_count(matches, processed)
    print("Doing something - update")
    return processed


def main():
    ctr = 0
    face_counter = None  # Will be created after first frame is captured
    # Set up image source
    cap = cv2.VideoCapture()

    cap.open(0)
    print(cap.isOpened())
    frame_number = -1
    while True:
        frame_number += 1
        ret, frame = cap.read()
        print(ret)

        if not ret:
            print("Error")
            break

        if face_counter is None:
            # We do this here, so that we can initialize with actual frame size
            face_counter = FaceCounter(frame.shape[:2], frame.shape[0] / 2)

        processed = process_frame(frame_number, frame, face_counter)

        cv2.imshow('Processed Image', processed)
        #        cv2.imshow('Webcam', frame)

        print("Doing something")

        k = cv2.waitKey(33)
        if k == 27:
            # Escape
            break

        ctr += 1

    cv2.destroyAllWindows()
    cap.release()


main()
