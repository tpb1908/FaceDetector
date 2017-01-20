import cv2

cap = cv2.VideoCapture()

print(cap.open(0))

while cap.isOpened():
    ret, frame = cap.read()

    cv2.imshow("Image", frame)
    k = cv2.waitKey(33)
    if k != -1:
        cap.release()

# Apparently CV2 windows are a bit shit, and so we have to try waitKey a few times for the window to close
cv2.waitKey(1)
cv2.destroyAllWindows()
for i in range(1, 5):
    cv2.waitKey(1)
