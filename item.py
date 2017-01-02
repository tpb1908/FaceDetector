import cv2
import random


class Item:
    def __init__(self, x = 0, y = 0):
        # Initialize item size
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.points = random.randint(30, 50)

    # Check for collision with another rectangle
    def is_colliding(self, x, y, width, height):
        return (not (not (self.x < x + width) or not (self.x + self.width > x) or not (self.y < y + height)) and
                self.height + self.y > y)

    # Draw the item to the frame
    def render(self, frame):
        cv2.rectangle(frame, (self.x, self.y), (self.x + self.width, self.y + self.height), (0, 0, 255), -1)

    def points(self):
        return self.points
