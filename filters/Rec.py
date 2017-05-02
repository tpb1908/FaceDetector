import openface
import cv2
import numpy as np
from random import randint
from ui.Painter import Painter

from filters.Filter import Filter


class Rec(Filter):

    NAME = "Recognition"

    aligner = openface.AlignDlib("./dlib_shape.dat")

    saved_faces = {}

    mode = 0

    def __init__(self, active=False):
        super(Rec, self).__init__(Rec.NAME, active)

    def process_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        text = "INVALID MODE"
        if self.mode == 0:
            text = "Bounding boxes"
        elif self.mode == 1:
            text = "Landmarks"
        elif self.mode == 2:
            text = "Align face"
        elif self.mode == 3:
            text = "Recognition"

        cv2.putText(frame, "Mode: {}".format(text), (20, 40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))

        new_faces = {}

        # Get all face positions in frame
        for bounding_box in self.aligner.getAllFaceBoundingBoxes(frame):
            Painter.rectangle(
                frame,
                bounding_box.left(), bounding_box.top(),
                bounding_box.right(), bounding_box.bottom(),
                self.random_color(),
                3)

            if self.mode == 0:
                continue

            # Find landmarks
            landmarks = self.aligner.findLandmarks(frame, bounding_box)
            if self.mode == 1:
                for (x, y) in landmarks:
                    cv2.circle(frame, (x, y), 2, (0, 255, 0), 2)
                continue

            # align face
            alignedFace = self.aligner.align(96, frame, bounding_box, landmarks,
                                        skipMulti=False)  # skip image if more than one face is detected

            if self.mode == 2:
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
            for color, feat in self.saved_faces.iteritems():
                # Check if they are the same person
                d = features - feat
                if np.dot(d, d) < 0.99:
                    draw_color = color

            if draw_color is None:
                # Face was not in previous frame so assign new color
                draw_color = self.random_color()

                # Update features
            new_faces[draw_color] = features

            # Draw box
            Painter.rectangle(
                frame,
                bounding_box.left(), bounding_box.top(),
                bounding_box.right(), bounding_box.bottom(),
                draw_color,
                3)

        return frame

    def set_mode(self, mode):
        self.mode = mode

    @staticmethod
    def random_color():
        return randint(0, 255), randint(0, 255), randint(0, 255)
