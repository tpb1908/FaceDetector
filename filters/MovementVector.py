import math
import cv2

from filters.Filter import Filter


class MovementVector(Filter):
    NAME = "Movement Vector"
    RETAIN = 20
    LENGTH = 50
    COLOR = (0, 255, 255)

    def __init__(self, active=False):
        super(MovementVector, self).__init__(MovementVector.NAME, active)
        self._people_positions = {}

    def process_frame(self, frame):
        if not self._sense:
            new_people_positions = {}

            for (_, person) in self._sense.live_people().iteritems():
                name = person.name()
                if name in self._people_positions:
                    new_people_positions[name] = self._people_positions[name]
                    if len(new_people_positions[name]) > MovementVector.RETAIN:
                        new_people_positions[name].pop(0)
                else:
                    new_people_positions[name] = []

                new_people_positions[name].append(person.centroid())

                a, b = self.linear_regression(new_people_positions[name][-min(4, len(new_people_positions[name])):])

                p1 = person.centroid()
                theta = -math.atan(b) - (3.141593653 * 1 / 2)
                # print(b, int(theta * 180/3.141592653))

                p2 = (
                    int(p1[0] + math.cos(theta) * MovementVector.LENGTH),
                    int(p1[1] + math.sin(theta) * MovementVector.LENGTH))
                # print (p1, p2)

                for point in new_people_positions[name]:
                    cv2.circle(frame, point, 3, (0, 255, 0), 3)

                cv2.line(frame, p1, p2, MovementVector.COLOR, 3)
                cv2.circle(frame, p2, 3, (255, 0, 0), 3)

                self._people_positions = new_people_positions
        
        return frame

    @staticmethod
    def linear_regression(positions):
        sum_x, sum_y, sum_x2, sum_y2, sum_xy = 0, 0, 0, 0, 0

        for x, y in positions:
            sum_x += x
            sum_y += y
            sum_x2 += x ** 2
            sum_y2 += y ** 2
            sum_xy += x * y

        n = len(positions)
        sxy = sum_xy - (sum_x * sum_y) / float(n)

        if sxy == 0:
            return 0, 0
        sxx = sum_x2 - (sum_x ** 2 / float(n))
        b = sxx / sxy
        a = (sum_y / n) - b * (sum_x / n)

        return a, b
