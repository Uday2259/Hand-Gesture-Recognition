import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mpDraw = mp.solutions.drawing_utils

        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(
                    img,
                    handLms,
                    self.mpHands.HAND_CONNECTIONS
                )

        return img

    def findPosition(self, img):
        lmList = []

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]

            for id, lm in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

        return lmList

    def fingersUp(self, lmList):
        fingers = []

        if len(lmList) == 0:
            return 0

        # Thumb
        if lmList[self.tipIds[0]][1] > lmList[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other four fingers
        for id in range(1, 5):
            if lmList[self.tipIds[id]][2] < lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return sum(fingers)
    def getIndexFingerTip(self, lmList):
        if len(lmList) != 0:
            return lmList[8][1], lmList[8][2]
        return None