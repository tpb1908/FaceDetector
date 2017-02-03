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
        self.filters = [
            CountingLine(self.webcam.width(), self.webcam.height()), 
            Recolour(self.webcam.width(), self.webcam.height())
        ]

    def loop(self):
        frame, webcam_open = self.webcam.next_frame()
        
        # Apply filters
        if webcam_open:
            for filter in self.filters:
                frame = filter.apply(frame)
    
        self.webcam.render(frame)
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

        # Start window
        self.loop()
        self.window.mainloop()

if __name__ == "__main__":
    # Disable deprecation warning
    def warn(*args, **kwargs):
        pass
    if not FaceDetector.DEBUG:
        warnings.warn = warn

    # Run the program
    FaceDetector().run()
