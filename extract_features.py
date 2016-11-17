# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 12:47:33 2016

@author: vs26
"""

import os
import glob
import cv2
import matplotlib.pyplot as plt
from matplotlib import cm

HAAR_CASCADE_FACE_XML = \
    "C:\\opencv\\sources\\data\\" + \
    "haarcascades_cuda\\haarcascade_frontalface_default.xml"

print HAAR_CASCADE_FACE_XML

face_cascade = cv2.CascadeClassifier()
assert (face_cascade.load(HAAR_CASCADE_FACE_XML) == True)

data_dir = "F:\\DataSet\\"

print data_dir

features = []

for i in range(1, 23):
    s_dir = os.path.join(data_dir, "s{}".format(i))
    jpgs = glob.glob("{}\\*.jpg".format(s_dir))

    for jpg in jpgs:
        img = cv2.imread(jpg)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(img_grey, 1.2, 3, minSize=(200, 200))
        print len(faces)
        if len(faces) < 1:
            continue

        x, y, w, h = faces[0]
        # cv2.rectangle(img_rgb, (x, y), (x+w, y+h), (255, 0, 0), 2)

        face_img = img_rgb[y:y + h, x:x + w, :]

        plt.imshow(face_img)

        break

    break
