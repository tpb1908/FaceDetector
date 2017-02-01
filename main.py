# -*- coding: utf-8 -*-
"""
Created on Wed Oct 05 12:46:24 2016

@author: johnsona15
"""

import cv2
import os
import glob
import time
import warnings

from skimage import transform
from scipy.fftpack import dct
import cPickle as Pickle

import Tkinter as tk
from PIL import Image, ImageTk

from Face import Face
from Person import Person
from Webcam import Webcam

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

# Load cascade
# Source: https://github.com/opencv/opencv/tree/master/data/haarcascades
HAAR_CASCADE_FACE_XML = "/cascades/haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier()
assert face_cascade.load(os.getcwd() + HAAR_CASCADE_FACE_XML)

# Map of names to active persons
people = {}

window = tk.Tk()
webcam = Webcam(window)

retain = 8
with open("face-model.pkl", "rb") as fh:
    clf, gmm, thresh = Pickle.load(fh)

names = {}

# Loading the people that we have enrolled
for idx, f_dir in enumerate(glob.glob("person_*")):
    names[idx] = f_dir.split("_")[1]

def detect_faces(frame):
    # Detect face positions in frame
    img_grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # possibly add minSize=(200, 200)
    faces = face_cascade.detectMultiScale(img_grey, 1.3, 5)
    
    matches = []
    for position in faces:
        face = Face(position, img_grey)
        
        # Check if we recognise the face
        impostor = gmm.score(face.features()) < thresh

        # Get the name of the face
        pred_name = "Impostor"
        if not impostor:
            pred_cls = clf.predict(face_x)[0]
            pred_name = names[pred_cls]

        # Update (or create) the person
        if pred_name in people:
            people[pred_name].update(face)
        else:
            people[pred_name] = Person(face, pred_name)

        # Add them to the list of matches
        matches.append(people[pred_name])

    return matches


def process_frame(frame):
    # Draw the boundary line
    # TODO Make the position optional so that we can detect line crossing anywhere, or multiple lines
    cv2.line(frame, (0, webcam.height() / 2), (webcam.width(), webcam.height() / 2), DIVIDER_COLOUR, 1)

    matches = detect_faces(frame)
    for person in matches:
        shape = person.shape()

        # Mark the bounding box and the centroid on the processed frame
        cv2.rectangle(frame, (shape.x, shape.y), (shape.x + shape.width - 1, shape.y + shape.height - 1), BOUNDING_BOX_COLOUR, 1)
        cv2.circle(frame, person.centroid(), 2, CENTROID_COLOUR, -1)

        name = person.name()
        if name in people:
            cv2.putText(
                frame, "{} {}".format(name, people[name].shape().y), (shape.x, shape.y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)
        else:
            # Person is new
            cv2.putText(
                frame, "{}".format(name), (x, y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)

    # Check if person has crossed the line
    for (name, person) in people.items():
        if person.has_crossed(webcam.height() / 2):
            print("{} crossed the line".format(name))
            person.count()

    # Remove people that we haven't detected for 3 seconds
    for (name, person) in people.items():
        if not person.active():
            print("deleting")
            del people[name]
    
    return frame

def recolor(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

def loop():
    webcam.render()
    window.after(10, loop)

def main():
    # Added window quit shortcut
    window.bind('<Escape>', lambda e: window.quit())
    
    # Create toolbar
    toolbar = tk.Menu(window)
    window.config(menu=toolbar)
    
    # Setup webcam menu
    webcam_menu = tk.Menu(toolbar)
    webcam_menu.add_command(label="Open", command=webcam.open)
    webcam_menu.add_command(label="Close", command=webcam.close)
    toolbar.add_cascade(label="Webcam", menu=webcam_menu)

    # Add filters to webcam
    webcam.add_filter(process_frame)
    webcam.add_filter(recolor)
    
    # Start window
    loop()
    window.mainloop()

main()