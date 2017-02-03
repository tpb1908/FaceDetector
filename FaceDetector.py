# -*- coding: utf-8 -*-
"""
Created on Wed Oct 05 12:46:24 2016

@author: johnsona15
"""
from collections import OrderedDict

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

        self.filters = OrderedDict()
        self.filters[CountingLine.NAME] = CountingLine(self.webcam.width(), self.webcam.height(), self.sense, True)
        self.filters[Recolour.NAME] = Recolour(self.webcam.width(), self.webcam.height(), True)

    def loop(self):
        frame, webcam_open = self.webcam.next_frame()
        
        # Apply filters
        if webcam_open:
            for filter_name in self.filters:
                frame = self.filters[filter_name].apply(frame)
    
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

        # Toggle filter menu callback
        def toggle_filter(name, on_var):
            def callback():
                self.filters[name].set_active(on_var.get())
                
            return callback

        # Setup filter menu
        filter_menu = tk.Menu(toolbar)
        for i, name in enumerate(self.filters):
            # Create menu item for filter
            menu_item_on = tk.BooleanVar(value=self.filters[name].is_active())
            menu_item = filter_menu.add_checkbutton(
                label=name, 
                command=toggle_filter(name, menu_item_on), 
                variable=menu_item_on, 
                onvalue=True, 
                offvalue=False)
        toolbar.add_cascade(label="Filters", menu=filter_menu)

        # Detector menu callback
        def set_detector(detector):
            return lambda: self.sense.set_detector(detector)

        # Setup detector menu
        detector_menu = tk.Menu(toolbar)
        detector_menu.add_command(label="cv2", command=set_detector(Cv2Detector()))
        detector_menu.add_command(label="dlib", command=set_detector(DlibDetector()))
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
