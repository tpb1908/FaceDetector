import cv2


cap = cv2.VideoCapture()

print(cap.open(0))

while True:
    ret, frame = cap.read()

    cv2.imshow("Image", frame)
    if cv2.waitKey(33) == 1048608:
        break

cv2.destroyAllWindows()
cap.release()
