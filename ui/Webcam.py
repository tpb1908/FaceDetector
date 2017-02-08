import Tkinter as tk
import numpy as np
from PIL import Image, ImageTk

import cv2


class Webcam(object):
    def __init__(self, root):
        # Setup widget
        self._root = root
        self._widget = tk.Label(root)
        self._widget.pack()

        def on_click(event):
            print "Event"

        self._widget.bind("<Button 1>", on_click)

        self._resize_callback = None

        self._capture = cv2.VideoCapture()
        self._capture.set(cv2.cv.CV_CAP_PROP_FPS, 30)
        self.open()

    def _set_size(self):
        # Sets the width and height of webcam frame
        ret, frame = self._capture.read()
        if not ret:
            self._width = 800
            self._height = 600
        else:
            frame_size = frame.shape[1::-1]
            self._width = frame_size[0]
            self._height = frame_size[1]

        if self._resize_callback is not None:
            self._resize_callback()

    def open(self, value=0):
        self._capture.open(value)
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
            frame = cv2.flip(frame, 1)
            return frame, True

        # No webcam input so return black image
        image = np.zeros((self._height, self._width, 3), np.uint8)
        # TODO: is there a better way to center text?
        cv2.putText(image, "Webcam Closed", (self._width / 2 - 60, self._height / 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 0, 0), 0)

        return image, False

    def is_open(self):
        return self._capture.isOpened()

    def on_resize(self, callback):
        self._resize_callback = callback

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height
