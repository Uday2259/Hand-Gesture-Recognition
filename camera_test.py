import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    success, img = cap.read()

    if not success:
        print("Failed")
        continue

    cv2.imshow("Camera Test", img)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()