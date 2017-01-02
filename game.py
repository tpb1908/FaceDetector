import cv2

# Initizlize camera
camera = cv2.VideoCapture()
camera.open(0)

while True:
    # Get the next webcam frame
    flag, frame = camera.read()
    cv2.imshow("Camera", frame)

    # Check for key press
    key = cv2.waitKey(33)
    if key != -1:
        # Exit game
        break

# Clean up
cv2.destroyAllWindows()
camera.release()