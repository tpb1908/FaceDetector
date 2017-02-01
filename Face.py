from skimage import transform
from scipy.fftpack import dct

class Face(object):
    RETAIN = 8
  
    def __init__(self, (x, y, width, height), image):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        
        # Crop the frame to the face
        image = image[y:y + h, x:x + w] 
        image = transform.resize(image, (w, h))

        # Extract features
        face_dct = dct(dct(image.T).T)
        self._features = face_dct[:RETAIN, :RETAIN].flatten().reshape((1, -1))

        # Find the centre of a face
    def centroid(self):
        return self._x + int(self._width / 2), self._y + int(self._height / 2)

    def features(self):
        return self._features

    def shape(self):
        return (x:self._x, y:self._y, w:self._width, h:self._height)

