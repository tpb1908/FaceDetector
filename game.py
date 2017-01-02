import cv2

class Game:
    def __init__(self):
        self.running = False

        # Initizlize camera
        self.camera = cv2.VideoCapture()
        self.camera.open(0)

    # Update method
    def update(self):
        # Get the next webcam frame
        flag, self.frame = self.camera.read()

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