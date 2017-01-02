import cv2

class Game:
    def __init__(self):
        self.running = False

        # Initizlize camera
        self.camera = cv2.VideoCapture()
        self.camera.open(0)

        # Load cascade
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Update method
    def update(self):
        # Get the next webcam frame
        flag, self.frame = self.camera.read()

        # Detect faces in frame
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, width, height) in faces:
            # Draw rectange around face
            cv2.rectangle(self.frame, (x, y), (x+width, y+height), (255, 0, 0), 2)

        # Check for key press
        key = cv2.waitKey(33)
        if key != -1:
            # Exit game
            self.running = False

    # Render method
    def render(self):
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