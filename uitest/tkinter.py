import Tkinter as tk

import cv2
import numpy as np
import sys

from PIL import Image, ImageTk

import bench

window = tk.Tk()
label = tk.Label(window)
sample = 0

def loop():
    global sample

    if sample >= bench.SAMPLES:
        bench.avg()
        sys.exit(0)

    print "Start loop"

    frame = np.zeros((600, 800, 3), np.uint8)

    bench.begin()
    image = Image.fromarray(frame)
    bench.end("image = Image.fromarray(frame)")

    bench.begin()
    tkimage = ImageTk.PhotoImage(image=image)
    bench.end("tkimage = ImageTk.PhotoImage(image=image)")

    bench.begin()
    label.imgtk = tkimage
    bench.end("label.imgtk = tkimage")

    bench.begin()
    label.configure(image=tkimage)
    bench.end("label.configure(image=tkimage)")

    sample+=1
    print "End loop\n"

    window.after(1, loop)

loop()
window.mainloop()