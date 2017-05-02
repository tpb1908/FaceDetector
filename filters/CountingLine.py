import cv2

from filters.Filter import Filter
from ui.Painter import Painter


class CountingLine(Filter):
    # Colours for drawing on processed frames
    DIVIDER_COLOUR = (255, 255, 0)
    BOUNDING_BOX_COLOUR = (255, 0, 0)
    CENTROID_COLOUR = (0, 0, 255)

    # Filter name
    NAME = "Counting Line"

    def __init__(self, line_pos, active=False):
        super(CountingLine, self).__init__(CountingLine.NAME, active)
        self._line_pos = line_pos

    def process_frame(self, frame):
        if self._sense is not None:
            filter = super(CountingLine, self)

            # Get the people in frame
            matches = self._sense.active_people()

            # Draw the boundary line
            Painter.line(frame,
                         0,
                         self._line_pos,
                         filter.width,
                         self._line_pos,
                          CountingLine.DIVIDER_COLOUR,
                         1)

            for _, person in matches.iteritems():

                # Check if person crossed the line
                if person.has_crossed(self._line_pos):
                    print("{} crossed the line".format(person.name()))
                    person.increment()

                shape = person.shape()

                # # Draw the bounding box
                # cv2.rectangle(frame,
                #               (shape.x, shape.y),
                #               (shape.x + shape.width - 1, shape.y + shape.height - 1),
                #               CountingLine.BOUNDING_BOX_COLOUR,
                #               1)
                #
                # Draw centroid
                cv2.circle(frame, person.centroid(), 2, CountingLine.CENTROID_COLOUR, -1)

                # Draw name and count
                cv2.putText(
                    frame, "{} {}".format(person.name(), person.count()),
                    (shape.x, shape.y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)

        return frame

    def set_line_pos(self, pos):
        print("Line pos set to " + str(pos))
        self._line_pos = int(self._height * pos / 100)
