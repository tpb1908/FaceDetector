import time

import cv2

from filters.Filter import Filter


class Info(Filter):

    NAME = "Info"

    def __init__(self, active=False):
        super(Info, self).__init__(Info.NAME, active)

    def process_frame(self, frame):
        width, height, channels = frame.shape
        cv2.putText(
            frame,
            "W{} H{} C{} T{}".format(width, height, channels, round(self._sense.detect_time(), 3)),
            (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)

        return frame
