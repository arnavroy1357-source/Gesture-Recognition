# Advanced Gesture AI

A real-time hand gesture recognition system built using Python, OpenCV, and MediaPipe. The application detects multiple hand gestures from a webcam feed, displays them in real time, and includes an air drawing feature controlled by hand gestures.

---

## Features

- Real-time hand tracking
- Supports tracking up to two hands simultaneously
- Gesture recognition with smoothing for stable predictions
- Air drawing using the index finger
- Dual-hand "Rock On" gesture detection (Spider-Man mode)
- Live FPS counter
- Low-light image enhancement
- Hand bounding boxes and labels
- Finger-tip highlighting
- Full-screen webcam interface

---

## Supported Gestures

| Gesture     |  Description                      |
|-------------|-----------------------------------|
| Open Palm   | All fingers extended              |
| Fist        | All fingers folded                |
| Pointing    | Index finger extended             |
| Peace       | Index and middle fingers extended |
| Rock On     | Index and pinky fingers extended  |
| Thumbs Up   | Thumb pointing upward             |
| Thumbs Down | Thumb pointing downward           |
| Pinch       | Thumb and index finger touching   |

---

## Special Features

### Air Drawing

Use the **Pointing** gesture to draw on the screen.

Press **C** to clear the drawing.

### Spider-Man Mode

When both hands perform the **Rock On** gesture simultaneously, the application displays:

```
Spider-Man
```

---

## Project Structure

```
Advanced-Gesture-AI/
│
├── gesture_app.py
└── README.md
```

---

## Requirements

- Python 3.10 or later
- OpenCV
- MediaPipe

---

## Installation

# install them manually:

```bash
pip install opencv-python mediapipe
```

---

## Running the Application

```bash
python gesture_app.py
```

---

## Controls

| Key  | Action                |
|------|-----------------------|
| Q    | Quit the application  |
| C    | Clear the air drawing |

---

## Display Information

The application displays the following in real time:

- Hand landmarks
- Bounding boxes
- Left/Right hand labels
- Detected gesture name
- Finger-tip highlights
- Air drawing
- FPS counter
- Gesture information box

---

## Technologies Used

- Python
- OpenCV
- MediaPipe Hands
- Math
- Collections (Deque and Counter)

---

## Future Improvements

- Gesture-controlled mouse
- Gesture-controlled volume
- Virtual keyboard
- Media controller
- Sign language recognition
- Custom gesture training
- Particle visual effects
- Face tracking integration

---

## Notes

- Ensure your webcam is connected before starting the application.
- Good lighting improves detection accuracy.
- Press **C** to clear the drawing.
- Press **Q** to exit the application.

---

## Author

**Arnav Roy**

Student, Developer, and AI & Computer Vision Enthusiast.

---

## License

This project is released under the MIT License.
