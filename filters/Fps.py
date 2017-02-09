import time

import cv2

from filters.Filter import Filter


class Fps(Filter):
    NAME = "Fps"

    def __init__(self, width, height, active=False):
        super(Fps, self).__init__(width, height, Fps.NAME, active)
        self._last_frame = time.time()

    def process_frame(self, frame):
        filter = super(Fps, self)

        # Get fps
        now = time.time()
        fps = 1 / (now - self._last_frame)

        cv2.putText(
            frame,
            "FPS: " + str(int(fps)),
            (filter.width - 80, 20),
            cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)
        self._last_frame = now
        return frame
