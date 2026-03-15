import cv2
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

canvas = None
# FIX 1: properly initialize two separate variables
prev_x, prev_y = 0, 0

# Fullscreen window
cv2.namedWindow("AIR DRAWING", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("AIR DRAWING", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

draw_color = (0, 255, 0)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)

    if canvas is None:
        canvas = np.zeros_like(frame)

    h, w, c = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

            index = handLms.landmark[8]
            middle = handLms.landmark[12]
            ix, iy = int(index.x * w), int(index.y * h)
            mx, my = int(middle.x * w), int(middle.y * h)

            # Draw when index finger is above middle finger
            if iy < my:
                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = ix, iy
                cv2.line(canvas, (prev_x, prev_y), (ix, iy), draw_color, 5)
                prev_x, prev_y = ix, iy
            else:
                prev_x, prev_y = 0, 0

            # FIX 4: color zones scale with frame width
            zone = w // 4
            if iy < 80:
                if ix < zone:
                    draw_color = (255, 0, 0)
                elif ix < zone * 2:
                    draw_color = (0, 255, 0)
                elif ix < zone * 3:
                    draw_color = (0, 0, 255)
                else:
                    canvas = np.zeros_like(frame)

    frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

    # FIX 4: buttons scale with frame width
    zone = w // 4
    cv2.rectangle(frame, (0, 0),          (zone, 80),      (255, 0, 0), -1)
    cv2.rectangle(frame, (zone, 0),       (zone*2, 80),    (0, 255, 0), -1)
    cv2.rectangle(frame, (zone*2, 0),     (zone*3, 80),    (0, 0, 255), -1)
    cv2.rectangle(frame, (zone*3, 0),     (w, 80),         (50, 50, 50), -1)
    cv2.putText(frame, "BLUE",  (zone*0+20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.putText(frame, "GREEN", (zone*1+20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.putText(frame, "RED",   (zone*2+20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.putText(frame, "CLEAR", (zone*3+20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    # FIX 2: consistent window name everywhere
    cv2.imshow("AIR DRAWING", frame)
    cv2.setWindowProperty("AIR DRAWING", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # FIX 3: only one waitKey call per loop
    key = cv2.waitKey(1)
    if key & 0xFF == ord('c'):
        canvas = np.zeros_like(frame)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()