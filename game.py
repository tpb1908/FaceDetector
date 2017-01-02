import cv2
import random
from item import Item

class Game:
    def __init__(self):
        self.running = False

        # Initizlize camera
        self.camera = cv2.VideoCapture()
        self.camera.open(0)
        self.width = self.camera.get(3)
        self.height = self.camera.get(4)

        # Load cascade
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # Initizile items
        self.items = []
        for _ in range(3):
            item = Item(random.randint(0, self.width-50), random.randint(0, self.height-50))
            self.items.append(item)

        # Initizle faces
        self.faces = []
        
    # Update method
    def update(self):
        # Get the next webcam frame
        flag, self.frame = self.camera.read()

        # Add items until their are 3
        while len(self.items) < 3:
            item = Item(random.randint(0, self.width-50), random.randint(0, self.height-50))
            self.items.append(item)

        # Detect faces in frame
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.2, 5, minSize=(150, 150))
        self.faces = []
        for (x, y, width, height) in faces:
            self.faces.append((x, y, width, height))

            # Check if face collides with any items
            for i in self.items:
                if i.isColliding(x, y, width, height):
                    self.items.remove(i)

        # Check for key press
        key = cv2.waitKey(33)
        if key != -1:
            # Exit game
            self.running = False

    # Render method
    def render(self):
        # Render items
        for i in self.items:
            i.render(self.frame)

        # Render faces
        for (x, y, width, height) in self.faces:
            cv2.rectangle(self.frame, (x, y), (x+width, y+height), (255, 0, 0), 2)

        # Push frame to window
        cv2.imshow("Camera", self.frame)

    # Starts the game loop
    def run(self):
        self.running = True
        while self.running:
            self.update()
            self.render()

    # Clean up any objects
    def destroy(self):
        # Clean up
        cv2.destroyAllWindows()
        self.camera.release()

game = Game()
game.run()
game.destroy()