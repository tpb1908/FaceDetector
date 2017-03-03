import cv2

from filters.Filter import Filter


class FaceHighlighter(Filter):
    # Colours for drawing on processed frames
    BOUNDING_BOX_COLOUR = (255, 0, 0)
    CENTROID_COLOUR = (0, 0, 255)

    # Filter name
    NAME = "Face Highlighter"

    def __init__(self, active=False):
        super(FaceHighlighter, self).__init__(FaceHighlighter.NAME, active)
        
    def process_frame(self, frame):
        if not self._sense == None:
            # Get the people in frame
            matches = self._sense.active_people()

            for _, person in matches.iteritems():

                shape = person.shape()

                # Draw the bounding box
                cv2.rectangle(frame,
                            (shape.x, shape.y),
                            (shape.x + shape.width - 1, shape.y + shape.height - 1),
                            FaceHighlighter.BOUNDING_BOX_COLOUR,
                            1)

                # Draw centroid
                # cv2.circle(frame, person.centroid(), 2, FaceHighlighter.CENTROID_COLOUR, -1)

                # Draw name and count
                cv2.putText(
                    frame, "{}".format(person.name()),
                    (shape.x, shape.y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)

        return frame
