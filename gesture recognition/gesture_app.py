
#Run:  python gesture_app.py




import cv2
import mediapipe as mp
import math
import time
from collections import deque, Counter

 
# MEDIAPIPE SETUP

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
 
# LANDMARK IDS
 
WRIST = 0

THUMB_TIP = 4
INDEX_TIP = 8
MIDDLE_TIP = 12
RING_TIP = 16
PINKY_TIP = 20

INDEX_PIP = 6
MIDDLE_PIP = 10
RING_PIP = 14
PINKY_PIP = 18


# GLOBALS

gesture_buffers = {
    "Left": deque(maxlen=5),
    "Right": deque(maxlen=5)
}

draw_points = []

# UTILITIES

def distance(a, b):

    return math.hypot(
        a.x - b.x,
        a.y - b.y
    )

def finger_up(lms, tip, pip):

    return lms[tip].y < lms[pip].y

def thumb_up(lms, handedness):

    if handedness == "Right":
        return lms[THUMB_TIP].x < lms[3].x

    return lms[THUMB_TIP].x > lms[3].x

def smooth_gesture(handedness, gesture):

    buffer = gesture_buffers[handedness]

    buffer.append(gesture)

    if len(buffer) < 3:
        return gesture

    return Counter(buffer).most_common(1)[0][0]

# GESTURE DETECTION

def detect_gesture(lms, handedness):

    thumb = thumb_up(lms, handedness)

    index = finger_up(
        lms,
        INDEX_TIP,
        INDEX_PIP
    )

    middle = finger_up(
        lms,
        MIDDLE_TIP,
        MIDDLE_PIP
    )

    ring = finger_up(
        lms,
        RING_TIP,
        RING_PIP
    )

    pinky = finger_up(
        lms,
        PINKY_TIP,
        PINKY_PIP
    )

    pinch_dist = distance(
        lms[THUMB_TIP],
        lms[INDEX_TIP]
    )


    #  GESTURES
    
                                                           
    if thumb and index and middle and ring and pinky:
        return "Open Palm"

                                                            
    if not thumb and not index and not middle \
       and not ring and not pinky:
        return "Fist"

    if index and not middle and not ring and not pinky:
        return "Pointing"

                                                            
    if index and middle and not ring and not pinky:
        return "Peace"

                                                          
    if index and pinky and not middle and not ring:
        return "Rock On"

    if thumb and not index and not middle \
       and not ring and not pinky:

        if lms[THUMB_TIP].y < lms[WRIST].y:
            return "Thumbs Up"

        return "Thumbs Down"

                                                           
        return "Pinch"

    return "Unknown"


# CENTER UI BOX

def draw_center_box(frame, text):

    h, w = frame.shape[:2]

    font = cv2.FONT_HERSHEY_SIMPLEX

    scale = 1.5

    thickness = 4

    (tw, th), _ = cv2.getTextSize(
        text,
        font,
        scale,
        thickness
    )

    x1 = (w - tw) // 2 - 40
    y1 = h - 150

    x2 = x1 + tw + 80
    y2 = y1 + 90

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (x1, y1),
        (x2, y2),
        (0, 0, 0),
        -1
    )

    cv2.addWeighted(
        overlay,
        0.5,
        frame,
        0.5,
        0,
        frame
    )

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        (0, 255, 0),
        3
    )

    cv2.putText(
        frame,
        text,
        (x1 + 20, y2 - 25),
        font,
        scale,
        (255, 255, 255),
        thickness
    )

# CAMERA

cap = cv2.VideoCapture(
    0,
    cv2.CAP_DSHOW
)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# WINDOW 

cv2.namedWindow(
    "Advanced Gesture AI",
    cv2.WINDOW_NORMAL
)

cv2.moveWindow(
    "Advanced Gesture AI",
    0,
    0
)

cv2.resizeWindow(
    "Advanced Gesture AI",
    1920,
    1080
)


# FPS

prev_time = time.time()


# MAIN LOOP

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    
    # LOW LIGHT OPTIMIZATION
    
    frame = cv2.convertScaleAbs(
        frame,
        alpha=1.2,
        beta=20
    )

    h, w = frame.shape[:2]

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = hands.process(rgb)

    detected_gestures = []
    
    # HAND DETECTION

    if results.multi_hand_landmarks:

        for idx, hand_landmarks in enumerate(
            results.multi_hand_landmarks
        ):

            handedness = results.multi_handedness[idx]\
                .classification[0].label

            lms = hand_landmarks.landmark

            
            # DRAW LANDMARKS
            
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_draw.DrawingSpec(
                    color=(255,255,255),
                    thickness=2,
                    circle_radius=3
                ),
                mp_draw.DrawingSpec(
                    color=(0,255,255),
                    thickness=2
                )
            )

            
            # BOUNDING BOX

            xs = [int(lm.x * w) for lm in lms]
            ys = [int(lm.y * h) for lm in lms]

            x1 = min(xs) - 20
            y1 = min(ys) - 20

            x2 = max(xs) + 20
            y2 = max(ys) + 20

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0,255,0),
                2
            )

            
            # HAND LABEL

            cv2.putText(
                frame,
                handedness,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,255),
                2
            )

            
            # GESTURE DETECTION
            

            gesture = detect_gesture(
                lms,
                handedness
            )

            gesture = smooth_gesture(
                handedness,
                gesture
            )

            detected_gestures.append(gesture)

            # DRAWING

            if gesture == "Pointing":

                ix = int(
                    lms[INDEX_TIP].x * w
                )

                iy = int(
                    lms[INDEX_TIP].y * h
                )

                draw_points.append(
                    (ix, iy)
                )

            
            # GESTURE LABEL

            cv2.putText(
                frame,
                gesture,
                (x1, y2 + 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0,255,255),
                2
            )

          
            # FINGER GLOW 

            for tip in [
                THUMB_TIP,
                INDEX_TIP,
                MIDDLE_TIP,
                RING_TIP,
                PINKY_TIP
            ]:

                x = int(lms[tip].x * w)
                y = int(lms[tip].y * h)

                cv2.circle(
                    frame,
                    (x, y),
                    12,
                    (255,255,0),
                    2
                )

    
    # DRAWING 
    
    for i in range(1, len(draw_points)):

        cv2.line(
            frame,
            draw_points[i - 1],
            draw_points[i],
            (255, 0, 255),
            5
        )

   
    #  SPIDER-MAN 
    
    if detected_gestures.count("Rock On") == 2:

        draw_center_box(
            frame,
            "Spider-Man"
        )

    elif len(detected_gestures) > 0:

        draw_center_box(
            frame,
            detected_gestures[0]
        )

    
    # FPS

    current_time = time.time()

    fps = 1 / max(
        current_time - prev_time,
        1e-6
    )

    prev_time = current_time

    cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )


    cv2.imshow(
        "Advanced Gesture AI",
        frame
    )

    key = cv2.waitKey(1)

    # Quit
    if key == ord("q"):
        break

    # Clear Drawing
    if key == ord("c"):
        draw_points.clear()
 
 

cap.release()
cv2.destroyAllWindows()