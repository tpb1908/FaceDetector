import Tkinter as tk
import time
import warnings
from collections import OrderedDict
import os
import openface
import cv2
import numpy as np
from random import randint

from ui.Webcam import Webcam


window = tk.Tk()
webcam = Webcam(window)

aligner = openface.AlignDlib("./dlib_shape.dat")

saved_faces = {}

mode = 0

def random_color():
    return (randint(0,255), randint(0,255), randint(0,255))

def loop():
    global saved_faces
    
    frame, webcam_open = webcam.next_frame()

    # Apply filters
    if webcam_open:
        # Convert to RGB
        print "Converting frame to RGB"
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        text = "INVALID MODE"
        if mode == 0:
            text = "Bounding boxes"
        elif mode == 1:
            text = "Landmarks"
        elif mode == 2:
            text = "Align face"
        elif mode == 3:
            text = "Recognition"
            
        cv2.putText(frame, "Mode: {}".format(text), (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))

        new_faces = {}

        # Get all face positions in frame
        for bounding_box in aligner.getAllFaceBoundingBoxes(frame):
            cv2.rectangle(
                frame, 
                (bounding_box.left(), bounding_box.top()), 
                (bounding_box.right(), bounding_box.bottom()),
                random_color(),
                3)

            if mode == 0:
                continue

            # Find landmarks
            landmarks = aligner.findLandmarks(frame, bounding_box)
            if mode == 1:
                for (x, y) in landmarks:
                    cv2.circle(frame, (x, y), 2, (0, 255, 0), 2)
                continue

            # align face
            alignedFace = aligner.align(96, frame, bounding_box, landmarks, skipMulti=False) # skip image if more than one face is detected
            
            if mode == 2:
                (ymax, xmax, _) = frame.shape
                print frame.shape
                for x in range(0, 96):
                    for y in range(0, 96):
                        for i in range(0, 3):
                            xpos = x + bounding_box.right() - int(0.5 * bounding_box.width()) - (96 / 2)
                            ypos = y + bounding_box.top() + int(0.5 * bounding_box.height()) - (96 / 2)
                            if xpos > xmax or ypos > ymax:
                                continue
                            frame[ypos][xpos][i] = alignedFace[y][x][i]

                continue

            # Extract features
            if alignedFace is not None:
                with openface.TorchNeuralNet(model="./nn4.small2.v1.t7") as net:
                    features = net.forward(alignedFace)

            draw_color = None
            for color, feat in saved_faces.iteritems():
                # Check if they are the same person
                d = features - feat
                if np.dot(d, d) < 0.99:
                    draw_color = color                

            if draw_color == None:
                # Face was not in previous frame so assign new color
                draw_color = random_color() 
    
            # Update features
            new_faces[draw_color] = features
            
            # Draw box
            cv2.rectangle(
                frame, 
                (bounding_box.left(), bounding_box.top()), 
                (bounding_box.right(), bounding_box.bottom()),
                draw_color,
                3)

        saved_faces = new_faces
    
    webcam.render(frame)
    window.after(1, loop)


# Added window quit shortcut
window.bind('<Escape>', lambda e: window.destroy())

# Modes
def change_mode(m):
    global mode
    mode = m

window.bind('1', lambda e: change_mode(0))
window.bind('2', lambda e: change_mode(1))
window.bind('3', lambda e: change_mode(2))
window.bind('4', lambda e: change_mode(3))

loop()
window.mainloop()