# Touchless Control

Control your computer using hand gestures and voice — no mouse or keyboard required.

**Touchless Control** is a real-time computer vision system that uses your webcam to track hand movements and convert them into mouse and system inputs. Now fully powered by a modern **Streamlit Web Dashboard**, you can configure settings and monitor gesture status in real-time.

<img width="800" height="455" alt="ezgif-4cc0666a0ad2ac23" src="https://github.com/user-attachments/assets/613cf67b-b64a-4ced-a0b1-69ca00bcf0fa" />

---

## Features

### Streamlit Web Dashboard
* Beautiful, modern dark-themed user interface.
* Real-time webcam feed with landmark overlays.
* Live status alerts for recognized gestures.
* Sidebar configuration panel to tweak smoothing and toggle specific gestures on/off.

### Gesture-Based Mouse Control
* **Move Cursor:** Point with your index finger.
* **Left Click:** Pinch your thumb and index finger together.
* **Drag & Drop:** Make a closed fist.
* **Scroll:** Hold up your index and middle fingers (move hand up/down to scroll).

### Voice Typing (Coming / In Progress)
* Speak to type anywhere on your system.
* Hands-free text input.
* Future: voice commands (open apps, shortcuts).

---

## How It Works

The system uses a real-time pipeline embedded inside a local web app:

1. **Web Dashboard** → Streamlit handles the UI, controls, and rendering.
2. **Webcam Input** → Captured asynchronously using OpenCV.
3. **Hand Tracking** → Powered by MediaPipe (21 landmark detection).
4. **Robust Gesture Recognition** → Math and geometry calculations map finger states (intentionally ignoring the thumb for stability during camera flips).
5. **System Control** → PyAutoGUI maps gestures to native OS actions.

## Gesture Controls

| Gesture                  | Action                        |
| ------------------------ | ----------------------------- |
| **Index finger up**      | Move cursor                   |
| **Pinch (thumb + index)**| Left click                    |
| **Fist**                 | Click & Drag                  |
| **Index + middle up**    | Scroll (Move hand up or down) |

---

## Installation & Usage

### Setup
1. Clone this repository.
2. Activate your virtual environment: `source .venv/bin/activate`
3. Install dependencies: `pip install -r reqs.txt`

### Running the App
Launch the web dashboard with a single command:
```bash
python run_app.py
```

---

## Inspiration

Inspired by the idea of replacing traditional input devices with natural human interaction, moving toward a more intuitive human-computer interface.
