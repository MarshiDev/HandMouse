import mediapipe
import cv2


# Initialize MediaPipe Hands.
hands = mediapipe.solutions.hands.Hands()

camera = cv2.VideoCapture(0)

hide = False


while True:
    cam_frame = camera.read()[1]
    rgb_frame = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2RGB)

    if hide:
        cam_frame.fill(0)

    # Process the frame with MediaPipe Hands.
    results = hands.process(rgb_frame)

    # Draw hand landmarks if detected.
    if results.multi_hand_landmarks:
        i = 0
        for hand_landmarks in results.multi_hand_landmarks:
            mediapipe.solutions.drawing_utils.draw_landmarks(
                cam_frame,
                hand_landmarks,
                mediapipe.solutions.hands.HAND_CONNECTIONS
            )

    cv2.imshow('Hand Landmarks Detection', cam_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.waitKey(1) & 0xFF == ord('h'):
        hide = not hide

camera.release()
cv2.destroyAllWindows()
hands.close()
