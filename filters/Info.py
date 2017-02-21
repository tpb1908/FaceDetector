import time

import cv2

from filters.Filter import Filter


class Info(Filter):

    NAME = "Info"

    def __init__(self, width, height, sense, active=False):
        super(Info, self).__init__(width, height, Info.NAME, sense, active)
        self._start_time = time.time()

    def process_frame(self, frame):
        width, height, channels = frame.shape
        cv2.putText(
            frame,
            "W{} H{} C{} T{}".format(width, height, channels, round(time.time()-self._start_time, 2)),
            (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)

        return frame
