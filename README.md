# Touchless Control

Control your computer using hand gestures and voice — no mouse or keyboard required.

**Touchless Control** is a real-time computer vision system that uses your webcam to track hand movements and convert them into mouse and system inputs. It also integrates voice recognition for hands-free typing.

---

## Features

### Gesture-Based Mouse Control

* Move cursor with your index finger
* Left click using pinch gesture
* Right click with finger combination
* Drag & drop using fist gesture
* Scroll using two fingers
* Pause control with open hand

### Voice Typing (Coming / In Progress)

* Speak to type anywhere on your system
* Hands-free text input
* Future: voice commands (open apps, shortcuts)

---

## How It Works

The system uses a real-time pipeline:

1. **Webcam Input** → Captured using OpenCV
2. **Hand Tracking** → Powered by MediaPipe (21 landmark detection)
3. **Gesture Recognition** → Finger state + distance calculations
4. **System Control** → PyAutoGUI maps gestures to OS actions

---

## Tech Stack

* Python
* OpenCV
* MediaPipe
* PyAutoGUI
* NumPy
* (Planned) SpeechRecognition / Pyttsx3

---

## Gesture Controls

| Gesture                  | Action      |
| ------------------------ | ----------- |
| Index finger             | Move cursor |
| Pinch (thumb + index)    | Left click  |
| Thumb + middle           | Right click |
| Fist                     | Drag        |
| Index + middle           | Scroll      |
| Open hand                | Pause       |

---

## Requirements

* Webcam
* Good lighting conditions
* Python 3.10 / 3.11 (recommended)
* Activate with source .venv/bin/activate (macOS)

---

##  Future Improvements

* Voice command system (open apps, shortcuts)
* Custom gesture mapping
* GUI interface for settings
* Multi-hand tracking
* Performance optimization

---

## Inspiration

Inspired by the idea of replacing traditional input devices with natural human interaction — moving toward a more intuitive human-computer interface.

---
