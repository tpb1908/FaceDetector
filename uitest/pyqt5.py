import sys

import cv2
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import bench

sample = 0


def loop():
    global sample

    if sample >= bench.SAMPLES:
        bench.avg()
        sys.exit(0)

    print "Start loop"

    frame = np.zeros((600, 800, 3), np.uint8)

    bench.begin()
    image = QImage(frame.tostring(), 800, 600, QImage.Format_RGB888).rgbSwapped()
    bench.end("image = QImage(frame.tostring(), 800, 600, QImage.Format_RGB888).rgbSwapped()")

    bench.begin()
    pixmap = QPixmap.fromImage(image)
    bench.end("pixmap = QPixmap.fromImage(image)")

    bench.begin()
    label.setPixmap(pixmap)
    bench.end("label.setPixmap(pixmap)")

    sample += 1

    print "End loop\n"


if __name__ == '__main__':
    # Create window
    app = QApplication(sys.argv)
    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Webcam test')
    w.show()

    # Added label and layout
    label = QLabel()
    vbox = QVBoxLayout()
    vbox.addWidget(label)
    w.setLayout(vbox)

    # Setup capture
    timer = QTimer()
    timer.timeout.connect(loop)
    timer.start(30)

    sys.exit(app.exec_())
