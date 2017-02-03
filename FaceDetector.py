# -*- coding: utf-8 -*-
"""
Created on Wed Oct 05 12:46:24 2016

@author: johnsona15
"""

import Tkinter as tk

from Webcam import Webcam

from filters.CountingLine import CountingLine
from filters.Recolour import Recolour

import warnings

class FaceDetector(object):
    DEBUG = False

    def __init__(self):
        self.window = tk.Tk()
        self.webcam = Webcam(self.window)


    def loop(self):
        self.webcam.render()
        self.window.after(10, self.loop)

    def run(self):
        # Added window quit shortcut
        self.window.bind('<Escape>', lambda e: self.window.quit())
        
        # Create toolbar
        toolbar = tk.Menu(self.window)
        self.window.config(menu=toolbar)
        
        # Setup webcam menu
        webcam_menu = tk.Menu(toolbar)
        webcam_menu.add_command(label="Open", command=self.webcam.open)
        webcam_menu.add_command(label="Close", command=self.webcam.close)
        toolbar.add_cascade(label="Webcam", menu=webcam_menu)

        # Add filters to webcam
        self.webcam.add_filter(CountingLine(self.webcam.width(), self.webcam.height()))
        self.webcam.add_filter(Recolour(self.webcam.width(), self.webcam.height()))

        # Start window
        self.loop()
        self.window.mainloop()

# Disable deprecation warning
def warn(*args, **kwargs):
    pass
if not FaceDetector.DEBUG:
    warnings.warn = warn

# Run the program
FaceDetector().run()
