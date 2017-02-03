import cv2

from filters.Filter import Filter

from sense.Person import Person

class CountingLine(Filter):
    # Colours for drawing on processed frames
    DIVIDER_COLOUR = (255, 255, 0)
    BOUNDING_BOX_COLOUR = (255, 0, 0)
    CENTROID_COLOUR = (0, 0, 255)

    # Filter name
    NAME = "Counting Line"

    def __init__(self, width, height, sense, active=False):
        super(CountingLine, self).__init__(width, height, CountingLine.NAME, active)
        self._sense = sense

    def process_frame(self, frame):
        # Draw the boundary line
        # TODO Make the position optional so that we can detect line crossing anywhere, or multiple lines
        filter = super(CountingLine, self)

        # Get the people in frame
        self._sense.proccess_frame(frame)
        matches = self._sense.live_people()

        cv2.line(frame, (0, filter.height() / 2), (filter.width(), filter.height() / 2),
                     CountingLine.DIVIDER_COLOUR, 1)

        for _, person in matches.iteritems():

            # Check if person crossed the line
            if person.has_crossed(super(CountingLine, self).height() / 2):
                print("{} crossed the line".format(person.name()))
                person.increment()

            shape = person.shape()

            # Draw the bounding box
            cv2.rectangle(frame,
                          (shape.x, shape.y),
                          (shape.x + shape.width - 1, shape.y + shape.height - 1),
                          CountingLine.BOUNDING_BOX_COLOUR,
                          1)
            
            # Draw centroid
            cv2.circle(frame, person.centroid(), 2, CountingLine.CENTROID_COLOUR, -1)

            # Draw name and count
            cv2.putText(
                frame, "{} {}".format(person.name(), person.count()), 
                (shape.x, shape.y - 5),
                cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)

        return frame