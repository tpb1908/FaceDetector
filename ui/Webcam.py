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
        self.open()
        
    def _set_size(self):
        # Sets the width and height of webcam frame
        ret, frame = self._capture.read()
        if not ret:
            print("Error getting frame size, couldnt read frame")
            return

        frame_size = frame.shape[1::-1]
        self._width = frame_size[0]
        self._height = frame_size[1]

    def open(self, value=0):
        assert self._capture.open(value)
        self._set_size()

    def close(self):
        self._capture.release()

    def render(self, frame):
        if self._widget is not None:
            image = Image.fromarray(frame)
            tkimage = ImageTk.PhotoImage(image=image)
            self._widget.imgtk = tkimage
            self._widget.configure(image=tkimage)
        else:
            print("ERROR: Webcam is not attached to a widget!")

    def next_frame(self):
        ret, frame = self._capture.read()
        if ret:
            return frame, True
        
        # No webcam input so return black image
        image = np.zeros((self._height, self._width , 3), np.uint8)
        # TODO: is their a better way to center text?
        cv2.putText(image, "Webcam Closed", (self._width / 2 - 60, self._height / 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 0)
        
        return image, False

    def is_open(self):
        return self._capture.isOpened()

    def width(self):
        return self._width

    def height(self):
        return self._height