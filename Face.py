from skimage import transform
from scipy.fftpack import dct
from collections import namedtuple

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

        # Extract features
        face_dct = dct(dct(image.T).T)
        self._features = face_dct[:Face.RETAIN, :Face.RETAIN].flatten().reshape((1, -1))

        # Find the centre of a face
    def centroid(self):
        return self._x + int(self._width / 2), self._y + int(self._height / 2)

    def features(self):
        return self._features

    def shape(self):
        return Face.Position(self._x, self._y, self._width, self._height)

