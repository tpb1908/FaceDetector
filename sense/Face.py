from skimage import transform
from scipy.fftpack import dct
from collections import namedtuple
import dlib
import numpy as np

class Face(object):
    RETAIN = 8
    Position = namedtuple('Position', ['x', 'y', 'width', 'height'])
    
    def __init__(self, (x, y, width, height), image):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        
        # Crop the frame to the face
        image = image[y:y + height, x:x + width] 
        image = transform.resize(image, (width, height))
        self._image = image

    @property
    def landmarks(self):
        return self._landmarks

    @landmarks.setter
    def landmarks(self, lm):
        self._landmarks = lm

    # Find the centre of a face
    def centroid(self):
        return self._x + int(self._width / 2), self._y + int(self._height / 2)

    def features(self):
        # Extract features
        face_dct = dct(dct(self._image.T).T)
        self._features = face_dct[:Face.RETAIN, :Face.RETAIN].flatten().reshape((1, -1))
        
        return self._features

    def shape(self):
        return Face.Position(self._x, self._y, self._width, self._height)

    def dlib_rect(self):
    
        return dlib.rectangle(self._x, self._y, self._x + self._width,self._y +  self._height)

    def image(self):
        return self._image

    def uint8_image(self):
        return (self._image * 255).astype(np.uint8)
