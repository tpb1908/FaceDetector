# -*- coding: utf-8 -*-
"""
Created on Wed Oct 05 12:46:24 2016

@author: johnsona15
"""
import Tkinter as tk
import time
import warnings
from collections import OrderedDict

from filters.CountingLine import CountingLine
from filters.Enrolment import Enrolment
from filters.EyeHighlighter import EyeHighlighter
from filters.FaceHighlighter import FaceHighlighter
from filters.FaceTransform import FaceTransform
from filters.Fps import Fps
from filters.Info import Info
from filters.Landmarks import Landmarks
from filters.Recolour import Recolour
from filters.Rec import  Rec
from modes.Capture import Capture
from modes.Main import Main
from sense.Sense import Sense
from sense.ThreadedSense import ThreadedSense
from sense.detection.Cv2Detection import Cv2Detection
from sense.detection.DlibDetection import DlibDetection
from ui.NameDialog import NameDialog
from ui.NumberDialog import NumberDialog
from ui.Webcam import Webcam


class FaceDetector(object):
    DEBUG = False

    def __init__(self):
        self.window = tk.Tk()
        self.webcam = Webcam(self.window)

        self.sense = Sense()

        self.active_mode = tk.StringVar(value=Main.NAME)

        self.modes = OrderedDict()
        self.modes[Main.NAME] = Main()
        self.modes[Capture.NAME] = Capture()

        self.filters = OrderedDict()
        self.filters[Fps.NAME] = Fps(True)
        self.filters[Info.NAME] = Info(False)
        self.filters[Landmarks.NAME] = Landmarks(False)
        self.filters[FaceHighlighter.NAME] = FaceHighlighter(True)
        self.filters[EyeHighlighter.NAME] = EyeHighlighter(True)
        self.filters[CountingLine.NAME] = CountingLine(self.webcam.height / 2, True)
        self.filters[Recolour.NAME] = Recolour(True)
        self.filters[FaceTransform.NAME] = FaceTransform(False)
        self.filters[Rec.NAME] = Rec(False)

        def change_mode(m):
            self.filters[Rec.NAME].set_mode(m)

        self.window.bind('1', lambda e: change_mode(0))
        self.window.bind('2', lambda e: change_mode(1))
        self.window.bind('3', lambda e: change_mode(2))
        self.window.bind('4', lambda e: change_mode(3))

    def loop(self):
        # TODO: handle timing better
        start = time.time()
        frame, webcam_open = self.webcam.next_frame()

        # Apply filters
        if webcam_open:
            self.sense.process_frame(frame)
            for filter in self.get_filters():
                frame = filter.apply(frame)

        start = time.time()
        self.webcam.render(frame)
        self.window.after(1, self.loop)

    def on_closing(self):
        self.window.destroy()

    def run(self):
        filter_menu = tk.Menu(self.window)
        filter_count = [0]  # We can't update  the count in update_filters

        # Toggle filter menu callback

        def toggle_filter(name, on_var):
            def callback():
                self.filters[name].set_active(on_var.get())

            return callback

        def update_filters():
            if filter_count[0] != 0:
                filter_menu.delete(0, filter_count[0])
            for filter in self.get_filters():
                filter.width = self.webcam.width
                filter.height = self.webcam.height
                filter.set_sense(self.sense)
                filter.set_mode(self.modes[self.active_mode.get()])

                menu_item_on = tk.BooleanVar(value=filter.is_active())
                filter_menu.add_checkbutton(
                    label=filter.NAME,
                    command=toggle_filter(filter.NAME, menu_item_on),
                    variable=menu_item_on,
                    onvalue=True,
                    offvalue=False)
                filter_count[0] += 1

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

        mode_menu = tk.Menu(toolbar)

        for _, key in enumerate(self.modes):
            mode_menu.add_radiobutton(label=key, variable=self.active_mode, command=update_filters)
        toolbar.add_cascade(label="Modes", menu=mode_menu)

        # Setup filter menu
        update_filters()
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
            NameDialog(self.window, lambda v: self.modes[Capture.NAME].set_enrollee(v))
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

    def get_filters(self):
        filtered = []
        for key, value in self.filters.items():
            if key in self.modes[self.active_mode.get()].filters():
                filtered.append(value)
        return filtered

if __name__ == "__main__":
    # Disable deprecation warning
    def warn(*args, **kwargs):
        pass


    if not FaceDetector.DEBUG:
        warnings.warn = warn

    # Run the program
    FaceDetector().run()