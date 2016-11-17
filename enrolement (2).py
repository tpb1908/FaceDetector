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
import glob

plt.close('all')

HAAR_CASCADE_FACE_XML = \
    "C:\\OpenCV Extract\\opencv\\sources\\data\\" + \
    "haarcascades_GPU\\haarcascade_frontalface_default.xml"

print (HAAR_CASCADE_FACE_XML)

face_cascade = cv2.CascadeClassifier()
assert(face_cascade.load(HAAR_CASCADE_FACE_XML) == True)

RED = (255, 0, 0)
RED_BGR = (0, 0, 255)

face_features = []
X_train = []
y_train = []

X_test = []
y_test = []
names = []

# ask for name
name = raw_input("What is your name?")
name = "person_{}".format(name)


#for idx, folder in enumerate(glob.glob('person_*')):
#    name = folder.split('_')[1]
#    names[idx] = name

# create folder of name
print "os path test "
if not os.path.exists(name):
    print "os path test sddfrtuy"
    os.makedirs(name)

# collect and save images using cv2
RETAIN = 8
W, H = 100, 100


def dct_2d(a):
    return dct(dct(a.T).T)
    
cap = cv2.VideoCapture()
print cap.open(0)

ctr = 0

while True:
    ret, img = cap.read()
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_grey, 1.3, 5) 
    # possibly add minSize=(200, 200) 
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), RED_BGR, 2)
        face_img = img_grey[y:y+h, x:x+w]
        face_img = transform.resize(face_img, (W, H))
        imsave(os.path.join(name, "{}_.png".format(ctr)), face_img)

    cv2.imshow('Webcam', img)
       
    k = cv2.waitKey(33)
    if k == 27:
        # Escape
        break

    ctr += 1 
    
    
cv2.destroyAllWindows()
cap.release()









