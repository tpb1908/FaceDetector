import cv2
import random
import time
from item import Item


class Game:
    def __init__(self):
        self.real_time = 0
        self.running = False
        self.playing = False
        self.points = 0
        self.time = 0
        self.faces = []
        self.items = []

        # Initialize camera
        self.camera = cv2.VideoCapture()
        self.camera.open(0)
        self.width = self.camera.get(3)
        self.height = self.camera.get(4)



        # Load cascade
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def reset(self):
        self.points = 0
        self.time = 0
        self.faces = []
        self.items = []

    # Update method
    def update(self, dt):
        # Get the next webcam frame
        flag, self.frame = self.camera.read()

        if self.playing:
            # Check if time is up
            self.time += dt
            if self.time >= 20:
                print self.points
                # Reset the game
                self.playing = False
                self.reset()
                
            # Continue with the game
            else:
                # Add items until their are 3
                while len(self.items) < 3:
                    item = Item(random.randint(0, self.width-50), random.randint(0, self.height-50))
                    self.items.append(item)   

                # Detect faces in frame
                gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                self.frame = gray
                cv_faces = self.face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(150, 150))
                self.faces = cv_faces
                for (x, y, width, height) in self.faces:
                    # Check if face collides with any items
                    for i in self.items:
                        if i.is_colliding(x, y, width, height):
                            self.points += i.points
                            self.items.remove(i)

        # Check for key press
        key = cv2.waitKey(33)
        if key == 1048603:
            # Escape key pressed, exit game
            self.running = False
        elif key == 1048608 and not self.playing:
            # Space key pressed, start game
            self.playing = True

    # Render method
    def render(self, dt):
        # Render items
        for i in self.items:
            i.render(self.frame)

        # Render faces
        for (x, y, width, height) in self.faces:
            cv2.rectangle(self.frame, (x, y), (x+width, y+height), (255, 0, 0), 2)

        if self.playing:
            # Render score
            text = "Score: " + str(self.points)
            cv2.putText(self.frame, text, (20, 40), cv2.FONT_ITALIC, 1, (0, 255, 0))

            # Render time
            text = "Time: " + str(int(20 - self.time))
            cv2.putText(self.frame, text, (20, 80), cv2.FONT_ITALIC, 1, (0, 255, 255)) 
        else:
            text = "Press space bar to start"
            (width, height), _ = cv2.getTextSize(text, cv2.FONT_ITALIC, 1, 3)
            cv2.putText(self.frame, text, (int(self.width/2 - width/2), int(self.height/2 - height/2)), cv2.FONT_ITALIC, 1, (0, 0, 0), 3)

        # Push frame to window
        cv2.imshow("Camera", self.frame)

    # Starts the game loop
    def run(self):
        self.running = True
        while self.running:
            current_time = time.time()
            self.update(current_time - self.real_time)
            self.render(current_time - self.real_time)
            self.real_time = current_time

    # Clean up any objects
    def destroy(self):
        # Clean up
        cv2.destroyAllWindows()
        self.camera.release()

game = Game()
game.run()
game.destroy()
