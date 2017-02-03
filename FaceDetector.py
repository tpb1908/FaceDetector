# -*- coding: utf-8 -*-
"""
Created on Wed Oct 05 12:46:24 2016

@author: johnsona15
"""

import Tkinter as tk

from ui.Webcam import Webcam

from filters.CountingLine import CountingLine
from filters.Recolour import Recolour

from sense.Cv2Recognition import Cv2Recognition
from sense.detectors.Cv2Detector import Cv2Detector 
from sense.detectors.DlibDetector import DlibDetector

import warnings

class FaceDetector(object):
    DEBUG = False

    def __init__(self):
        self.window = tk.Tk()
        self.webcam = Webcam(self.window)

        self.sense = Cv2Recognition(Cv2Detector())

        self.filters = {
            CountingLine.NAME: CountingLine(self.webcam.width(), self.webcam.height(), self.sense),
            Recolour.NAME: Recolour(self.webcam.width(), self.webcam.height())
        }
        self.active_filters = [CountingLine.NAME, Recolour.NAME]

    def loop(self):
        frame, webcam_open = self.webcam.next_frame()
        
        # Apply filters
        if webcam_open:
            for filter_name in self.active_filters:
                frame = self.filters[filter_name].apply(frame)
    
        self.webcam.render(frame)
        self.window.after(10, self.loop)

    def toggle_filter(self, name):
        return lambda: self.active_filters.remove(name) if name in self.active_filters else self.active_filters.append(name) 

    def set_detector(self, detector):
        return lambda: self.sense.set_detector(detector)

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

        # Setup filter menu
        filter_menu = tk.Menu(toolbar)
        for name in self.filters:
            filter_menu.add_command(label=name, command=self.toggle_filter(name))
        toolbar.add_cascade(label="Filters", menu=filter_menu)

        # Setup detector menu
        detector_menu = tk.Menu(toolbar)
        detector_menu.add_command(label="cv2", command=self.set_detector(Cv2Detector()))
        detector_menu.add_command(label="dlib", command=self.set_detector(DlibDetector()))
        toolbar.add_cascade(label="Detectors", menu=detector_menu)

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
