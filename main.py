# -*- coding: utf-8 -*-
"""
Created on Wed Oct 05 12:46:24 2016

@author: johnsona15
"""

import warnings
import Tkinter as tk

from Webcam import Webcam

from filters.CountingLine import CountingLine
from filters.Recolour import Recolour

DEBUG = False


# Disable deprecation warning
def warn(*args, **kwargs):
    pass
if not DEBUG:
    warnings.warn = warn


window = tk.Tk()
webcam = Webcam(window)


def loop():
    webcam.render()
    window.after(10, loop)


def main():
    # Added window quit shortcut
    window.bind('<Escape>', lambda e: window.quit())
    
    # Create toolbar
    toolbar = tk.Menu(window)
    window.config(menu=toolbar)
    
    # Setup webcam menu
    webcam_menu = tk.Menu(toolbar)
    webcam_menu.add_command(label="Open", command=webcam.open)
    webcam_menu.add_command(label="Close", command=webcam.close)
    toolbar.add_cascade(label="Webcam", menu=webcam_menu)

    # Add filters to webcam
    webcam.add_filter(CountingLine(webcam.width(), webcam.height()))
    webcam.add_filter(Recolour(webcam.width(), webcam.height()))

    # Start window
    loop()
    window.mainloop()

main()
