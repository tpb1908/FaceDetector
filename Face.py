from skimage import transform
from scipy.fftpack import dct

class Face(object):

    def __init__(self, (x, y, w, h), image):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        
        # This will crop the frame to the face
        image = image[y:y + h, x:x + w] 
        image = transform.resize(image, (w, h))

        # 2d-dct and truncate
        face_dct = dct(dct(image.T).T)
        retain = 8
        self._features = face_dct[:retain, :retain].flatten().reshape((1, -1))

        # Find the centre of a face
    def centroid(self):
        return self._x + int(self._w / 2), self._y + int(self._h / 2)

    def features(self):
        return self._features

    def shape(self):
        return (x:self._x, y:self._y, w:self._w, h:self._h)

