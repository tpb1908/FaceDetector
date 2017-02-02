import cv2
import numpy as np

import Tkinter as tk
from PIL import Image, ImageTk

from filters.Filter import Filter

class Webcam(object):
    def __init__(self, root):
        # Setup widget
        self._root = root
        self._widget = tk.Label(root)
        self._widget.pack()

        self._capture = cv2.VideoCapture()
        self._width = 800
        self._height = 600

        self._filters = []

        self.open()

    def open(self):
        assert self._capture.open(0)

    def close(self):
        self._capture.release()

    def add_filter(self, filter):
        if not isinstance(filter, Filter): 
            print("Filter is not a filter")
            return 
        self._filters.append(filter)

    def render(self):
        if not self._widget == None:
            frame = self.frame()
            for filter in self._filters:
                frame = filter.apply(frame)

            image = Image.fromarray(frame)
            tkimage = ImageTk.PhotoImage(image=image)
            self._widget.imgtk = tkimage
            self._widget.configure(image=tkimage)
        else:
            print("ERROR: Webcam is not attached to a widget!")

    def frame(self):
        ret, frame = self._capture.read()
        if ret:
            # Set webcam size
            frame_size = frame.shape[1::-1]
            self._width = frame_size[0]
            self._height = frame_size[1]

            return frame
        else:
            # No webcam input so return black image
            image = np.zeros((self._height, self._width , 3), np.uint8)
            # TODO: is their a better way to center text?
            cv2.putText(image, "Webcam Closed", (self._width / 2 - 60, self._height / 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 0)
            
            return image

    def is_open(self):
        return self._capture.isOpened()

    def width(self):
        return self._width

    def height(self):
        return self._height