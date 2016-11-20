import cv2

cap = cv2.VideoCapture()

print(cap.open(0))

while True:
    ret, frame = cap.read()

    cv2.imshow("Image", frame)
    k = cv2.waitKey(33)
    if k != -1:
        break

cv2.destroyAllWindows()
cap.release()
