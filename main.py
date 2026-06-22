import cv2
import numpy as np
from hand_detector import HandDetector

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

detector = HandDetector()

xp, yp = 0, 0

canvas = np.zeros((480, 640, 3), np.uint8)

while True:
    success, img = cap.read()

    if not success:
        break

    img = cv2.flip(img, 1)

    img = detector.findHands(img)

    lmList = detector.findPosition(img)

    if len(lmList) != 0:

        totalFingers = detector.fingersUp(lmList)

        x1, y1 = lmList[8][1], lmList[8][2]

        # One finger = Draw
        if totalFingers == 1:

            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)

            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            cv2.line(canvas, (xp, yp), (x1, y1), (255, 0, 255), 5)

            xp, yp = x1, y1

        # Open palm = Clear screen
        elif totalFingers == 5:

            canvas = np.zeros((480, 640, 3), np.uint8)

            xp, yp = 0, 0

        else:
            xp, yp = 0, 0

    imgGray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)

    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, canvas)

    cv2.putText(
        img,
        "1 Finger = Draw | 5 Fingers = Clear",
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.imshow("Air Writing", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()