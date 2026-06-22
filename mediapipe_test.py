import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

mp_draw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()

    if not success:
        continue

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    print("Hands Found:", results.multi_hand_landmarks is not None)

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                img,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

    cv2.imshow("MediaPipe Test", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()