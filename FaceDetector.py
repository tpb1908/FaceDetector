# -*- coding: utf-8 -*-
"""
Created on Wed Oct 05 12:46:24 2016

@author: johnsona15
"""
import Tkinter as tk
import warnings
import time
from collections import OrderedDict

from filters.CountingLine import CountingLine
from filters.Fps import Fps
from filters.Info import Info
from filters.Recolour import Recolour
from filters.EyeHighlighter import EyeHighlighter
from filters.MovementVector import MovementVector
from filters.FaceHighlighter import FaceHighlighter
from filters.Landmarks import Landmarks
from sense.detectors.Cv2Detector import Cv2Detector
from sense.detectors.DlibDetector import DlibDetector
from sense.thread.DetectorThread import DetectorThread
from sense.Cv2Recognition import Cv2Recognition
from ui.Webcam import Webcam
from ui.NumberDialog import NumberDialog


class FaceDetector(object):
    DEBUG = False

    def __init__(self):
        self.window = tk.Tk()
        self.webcam = Webcam(self.window)

        self.sense = DetectorThread(Cv2Detector())
        self.sense.start()

        self.filters = OrderedDict()
        self.filters[Fps.NAME] = Fps(self.webcam.width, self.webcam.height, True)
        self.filters[Info.NAME] = Info(self.webcam.width, self.webcam.height, False)
        self.filters[MovementVector.NAME] = MovementVector(self.webcam.width, self.webcam.height, self.sense, False)
        self.filters[Landmarks.NAME] = Landmarks(self.webcam.width, self.webcam.height, self.sense, True)
        self.filters[FaceHighlighter.NAME] = FaceHighlighter(self.webcam.width, self.webcam.height, self.sense, True)
        self.filters[EyeHighlighter.NAME] = EyeHighlighter(self.webcam.width, self.webcam.height, self.sense, True)
        self.filters[CountingLine.NAME] = CountingLine(self.webcam.width, self.webcam.height, self.sense,
                                                       self.webcam.height / 2, True)

        self.filters[Recolour.NAME] = Recolour(self.webcam.width, self.webcam.height, self.sense, True)

    def loop(self):
        start = time.time()
        frame, webcam_open = self.webcam.next_frame()
        print("Get frame: " + str(1000 * (time.time() - start)))
        # Apply filters
        if webcam_open:
            self.sense.update_frame(frame)
            for filter_name in self.filters:
                # start = time.time()
                frame = self.filters[filter_name].apply(frame)
                # print(filter_name + " " + str(1000 *(time.time() - start)))
        start = time.time()
        self.webcam.render(frame)
        print("Render frame: " + str(1000 * (time.time() - start)))
        self.window.after(1, self.loop)

    def on_closing(self):
        print "Closing"
        self.sense.kill()
        self.window.destroy()

    def run(self):
        # Setup resize event
        def resize():
            for (_, filter) in self.filters.items():
                filter.width = self.webcam.width
                filter.height = self.webcam.height

        self.webcam.on_resize(resize)

        # Added window quit shortcut
        self.window.bind('<Escape>', lambda e: self.on_closing())

        # Create toolbar
        toolbar = tk.Menu(self.window)
        self.window.config(menu=toolbar)

        # Setup webcam menu 
        webcam_menu = tk.Menu(toolbar)
        webcam_menu.add_command(label="Open", command=self.webcam.open)
        webcam_menu.add_command(label="Video", command=lambda: self.webcam.open('data/Sample.mp4'))
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
            filter_menu.add_checkbutton(
                label=name,
                command=toggle_filter(name, menu_item_on),
                variable=menu_item_on,
                onvalue=True,
                offvalue=False)
        toolbar.add_cascade(label="Filters", menu=filter_menu)

        # Setup detector menu
        detector_menu = tk.Menu(toolbar)
        detector_var = tk.StringVar(value="cv2")

        # Detector menu callback
        def set_detector():
            if detector_var.get() == "cv2":
                self.sense.set_detector(Cv2Detector())
            else:
                self.sense.set_detector(DlibDetector())

        detector_menu.add_radiobutton(label="cv2", variable=detector_var, command=set_detector)
        detector_menu.add_radiobutton(label="dlib", variable=detector_var, command=set_detector)

        toolbar.add_cascade(label="Detectors", menu=detector_menu)

        settings_menu = tk.Menu(toolbar)

        def show_dialog():
            NumberDialog(self.window, lambda v: self.filters[CountingLine.NAME].set_line_pos(v))

        settings_menu.add_command(label="Counting line", command=show_dialog)
        
        thread_var = tk.IntVar(value=1)

        def toggle_thread():
            self.sense.dispose()
            
            if thread_var.get() == 1:
                self.sense = DetectorThread(Cv2Detector())
            else:
                self.sense = Cv2Recognition(Cv2Detector())
            
            for filter in self.filters:
                filter.set_sense(self.sense)

        settings_menu.add_checkbutton(label="Threaded", var=thread_var, command=toggle_thread)

        toolbar.add_cascade(label="Settings", menu=settings_menu)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

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
