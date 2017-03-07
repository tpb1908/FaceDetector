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
from filters.Enrolment import Enrolment
from filters.Fps import Fps
from filters.Info import Info
from filters.Recolour import Recolour
from filters.EyeHighlighter import EyeHighlighter
from filters.MovementVector import MovementVector
from filters.FaceHighlighter import FaceHighlighter
from filters.Landmarks import Landmarks
from filters.FaceTransform import FaceTransform

from sense.detection.Cv2Detection import Cv2Detection
from sense.detection.DlibDetection import DlibDetection
from sense.Sense import Sense
from sense.ThreadedSense import ThreadedSense

from ui.Webcam import Webcam
from ui.NumberDialog import NumberDialog
from ui.NameDialog import NameDialog


class FaceDetector(object):
    DEBUG = False

    def __init__(self):
        self.window = tk.Tk()
        self.webcam = Webcam(self.window)

        self.sense = Sense()

        self.filters = OrderedDict()
        self.filters[Fps.NAME] = Fps(True)
        self.filters[Info.NAME] = Info(False)
        self.filters[MovementVector.NAME] = MovementVector(False)
        self.filters[Landmarks.NAME] = Landmarks(True)
        self.filters[FaceHighlighter.NAME] = FaceHighlighter(True)
        self.filters[EyeHighlighter.NAME] = EyeHighlighter(True)
        self.filters[CountingLine.NAME] = CountingLine(self.webcam.height / 2, True)
        self.filters[Recolour.NAME] = Recolour(True)
        self.filters[FaceTransform.NAME] = FaceTransform(False)

    def loop(self):
        # TODO: handle timing better
        start = time.time()
        frame, webcam_open = self.webcam.next_frame()
        
        # Apply filters
        if webcam_open:
            self.sense.process_frame(frame)
            for filter_name in self.filters:
                frame = self.filters[filter_name].apply(frame)
        
        start = time.time()
        self.webcam.render(frame)
        self.window.after(1, self.loop)

    def on_closing(self):
        self.window.destroy()

    def run(self):
        def update_filters():
            for (_, filter) in self.filters.items():
                filter.width = self.webcam.width
                filter.height = self.webcam.height
                filter.set_sense(self.sense)
        update_filters()
        
        # Setup resize event
        self.webcam.on_resize(update_filters)

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
        detection_menu = tk.Menu(toolbar)
        detection_var = tk.StringVar(value="dlib")

        # Detector menu callback
        def set_detection():
            if detection_var.get() == "cv2":
                self.sense.set_detection(Cv2Detection())
            else:
                self.sense.set_detection(DlibDetection())

        detection_menu.add_radiobutton(label="cv2", variable=detection_var, command=set_detection)
        detection_menu.add_radiobutton(label="dlib", variable=detection_var, command=set_detection)

        toolbar.add_cascade(label="Detection", menu=detection_menu)

        settings_menu = tk.Menu(toolbar)

        def show_counting_line_dialog():
            NumberDialog(self.window, lambda v: self.filters[CountingLine.NAME].set_line_pos(v))

        settings_menu.add_command(label="Counting line", command=show_counting_line_dialog)

        def show_enrolment_dialog():
            NameDialog(self.window, lambda v: self.filters[Enrolment.NAME].start(v))
            pass

        settings_menu.add_command(label="Enrolment", command=show_enrolment_dialog)

        thread_var = tk.IntVar(value=(type(self.sense) is ThreadedSense))

        def toggle_thread():
            if thread_var.get() == 1:
                self.sense = Sense()
            else:
                self.sense = ThreadedSense()
            
            update_filters()

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
