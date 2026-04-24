import streamlit as st
import cv2
import numpy as np
import time
from vision import Vision
from controller import Controller
from gestures import get_fingers, is_pinch
from config import config

st.set_page_config(page_title="Touchless Control", page_icon="🖱️", layout="wide")

# Custom CSS for modern styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stButton>button {
        background: linear-gradient(135deg, #6e8efb, #a777e3);
        color: white;
        border-radius: 8px;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
    }
    .alert-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #2e3136;
        border-left: 5px solid #a777e3;
        margin-bottom: 20px;
        font-size: 1.2rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("✨ Touchless Control Center")
st.markdown("Control your computer using hand gestures powered by AI.")

# Initialize session state variables
if "run" not in st.session_state:
    st.session_state.run = False

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    config.SMOOTHING = st.slider("Smoothing", 1, 15, config.SMOOTHING)
    config.ENABLE_CLICK = st.checkbox("Enable Click (Pinch)", config.ENABLE_CLICK)
    config.ENABLE_DRAG = st.checkbox("Enable Drag (Fist)", config.ENABLE_DRAG)
    config.ENABLE_SCROLL = st.checkbox("Enable Scroll (Two Fingers)", config.ENABLE_SCROLL)
    
    st.markdown("---")
    st.subheader("Controls")
    
    col1, col2 = st.columns(2)
    if col1.button("▶️ Start", use_container_width=True):
        st.session_state.run = True
    if col2.button("⏹️ Stop", use_container_width=True):
        st.session_state.run = False

# Layout
main_col, side_col = st.columns([3, 1])

frame_placeholder = main_col.empty()
alert_placeholder = side_col.empty()
stats_placeholder = side_col.empty()

@st.cache_resource
def get_components():
    return Vision(), Controller()

vision, controller = get_components()

# Prev x, y for smoothing
if 'prev_x' not in st.session_state:
    st.session_state.prev_x = 0
if 'prev_y' not in st.session_state:
    st.session_state.prev_y = 0

def smooth(x, y):
    st.session_state.prev_x += (x - st.session_state.prev_x) / config.SMOOTHING
    st.session_state.prev_y += (y - st.session_state.prev_y) / config.SMOOTHING
    return st.session_state.prev_x, st.session_state.prev_y

if st.session_state.run:
    if "cap" not in st.session_state:
        st.session_state.cap = cv2.VideoCapture(0)
    
    cap = st.session_state.cap
    ret, frame = cap.read()
    if not ret:
        st.error("Failed to access webcam.")
        st.session_state.run = False
        st.rerun()
        
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    
    # Process frame to get landmarks
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = vision.hands.process(rgb)
    
    current_gesture = "None"
    
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            vision.drawer.draw_landmarks(
                frame,
                hand_landmarks,
                vision.mp_hands.HAND_CONNECTIONS
            )
            
            # Custom Gesture Logic for the stream
            lm = hand_landmarks.landmark
            fingers = get_fingers(lm)
            
            # Mouse Movement
            x = int(lm[8].x * w)
            y = int(lm[8].y * h)
            
            # Map to screen (assuming 1920x1080)
            screen_x = np.interp(x, (100, w - 100), (0, 1920))
            screen_y = np.interp(y, (100, h - 100), (0, 1080))
            
            sx, sy = smooth(screen_x, screen_y)
            
            # Only point index finger -> Move
            if fingers == [0, 1, 0, 0, 0]:
                controller.move(sx, sy)
                current_gesture = "Moving 🖱️"
                
            # Pinch -> Click
            elif is_pinch(lm):
                if config.ENABLE_CLICK:
                    controller.click()
                    current_gesture = "Clicking 👆"
                    
            # Fist -> Drag
            elif fingers == [0, 0, 0, 0, 0]:
                if config.ENABLE_DRAG:
                    controller.drag(True)
                    current_gesture = "Dragging ✊"
            else:
                if config.ENABLE_DRAG:
                    controller.drag(False)
                    
            # Two fingers -> Scroll
            if fingers == [0, 1, 1, 0, 0] and not is_pinch(lm):
                if config.ENABLE_SCROLL:
                    # Simple scroll based on y position of hand
                    if y < h/3:
                        controller.scroll(1)
                        current_gesture = "Scrolling Up ⬆️"
                    elif y > 2*h/3:
                        controller.scroll(-1)
                        current_gesture = "Scrolling Down ⬇️"
                    else:
                        current_gesture = "Scroll Ready ↕️"
                        
    # Convert frame for Streamlit
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_placeholder.image(frame, channels="RGB", use_column_width=True)
    
    # Update Alerts
    alert_placeholder.markdown(f'<div class="alert-box">Status: {current_gesture}</div>', unsafe_allow_html=True)
    
    # Trigger a rerun to get the next frame
    time.sleep(0.01)
    st.rerun()

else:
    if "cap" in st.session_state:
        st.session_state.cap.release()
        del st.session_state.cap
    frame_placeholder.info("Click 'Start' in the sidebar to begin camera capture.")
    alert_placeholder.empty()
