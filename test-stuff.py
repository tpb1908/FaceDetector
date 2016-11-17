# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# import numpy as np
# import scipy
# import matplotlib.pyplot as plt
# from scipy import misc
import cv2
import os

cv2.__version__

imagePath = 'F:\DataSet\s1\s1l.jpg'

if not os.path.exists(imagePath):
    print "Can't find image..."

cascPath = 'haarcascade_frontalface_default.xml'

faceCascade = cv2.CascadeClassifier(cascPath)

image = cv2.imread(imagePath)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 5, minSize = (30,30), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
#
# print "Found {0} faces!".format(len(faces))
#
#
# for (x, y, w, h) in faces:
#    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
#    
# cv2.imshow("Faces found" ,image)
# cv2.waitKey(0)

# f = misc.imread('F:\DataSet\s1\s1l.jpg')
#
# plt.imshow(f, cmap=plt.cm.gray)
#
# plt.show()
#
# misc.imsave('faces.png', face)
#
# face = misc.imread('faces.png')
#
# type(face)
#
# face.shape, face.dtype
#
# face.tofile('face.raw')
#
# face_from_raw = np.fromfile('face.raw', dtype=np.uint8)
#
# face_from_raw.shape
#
# face_from_raw.shape = (768, 1024, 3)
# face_memmap = np.memmap('face.raw', dtype=np.uint8, shape=(768, 1024, 3))
