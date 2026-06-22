import cv2
from hand_detector import HandDetector

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

detector = HandDetector()

while True:
    success, img = cap.read()

    if not success:
        break

    img = detector.findHands(img)

    lmList = detector.findPosition(img)

    if len(lmList) != 0:

        totalFingers = detector.fingersUp(lmList)

        # Gesture Recognition
        if totalFingers == 0:
            gesture = "Fist"

        elif totalFingers == 1:
            gesture = "One Finger"

        elif totalFingers == 2:
            gesture = "Victory"

        elif totalFingers == 3:
            gesture = "Three Fingers"

        elif totalFingers == 4:
            gesture = "Four Fingers"

        elif totalFingers == 5:
            gesture = "Open Palm"

        else:
            gesture = "Unknown"

        cv2.putText(
            img,
            f'Gesture: {gesture}',
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 255, 0),
            3
        )

        cv2.putText(
            img,
            f'Fingers: {totalFingers}',
            (20, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (255, 0, 0),
            3
        )

    cv2.imshow("Gesture Recognition", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()