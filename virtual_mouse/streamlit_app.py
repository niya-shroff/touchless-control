import streamlit as st
import cv2
import numpy as np
import time
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import av

from vision import Vision
from controller import Controller
from gestures import get_fingers, is_pinch
from config import config

st.set_page_config(page_title="Touchless Control", page_icon="🖱️", layout="wide")

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
    </style>
""", unsafe_allow_html=True)

st.title("✨ Touchless Control Center")
st.markdown("Control your computer using hand gestures. **(Powered by WebRTC)**")

with st.sidebar:
    st.header("⚙️ Settings")
    config.SMOOTHING = st.slider("Smoothing", 1, 15, config.SMOOTHING)
    config.ENABLE_CLICK = st.checkbox("Enable Click (Pinch)", config.ENABLE_CLICK)
    config.ENABLE_DRAG = st.checkbox("Enable Drag (Fist)", config.ENABLE_DRAG)
    config.ENABLE_SCROLL = st.checkbox("Enable Scroll (Two Fingers)", config.ENABLE_SCROLL)

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

class VideoProcessor(VideoTransformerBase):
    def __init__(self):
        self.vision = Vision()
        self.controller = Controller()
        self.prev_x = 0
        self.prev_y = 0
        self.last_time = time.time()

    def smooth(self, x, y):
        self.prev_x += (x - self.prev_x) / config.SMOOTHING
        self.prev_y += (y - self.prev_y) / config.SMOOTHING
        return self.prev_x, self.prev_y

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1)
        h, w, _ = img.shape
        
        current_time = time.time()
        fps = 1.0 / (current_time - self.last_time + 1e-5)
        self.last_time = current_time
        
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = self.vision.hands.process(rgb)
        
        current_gesture = "None"
        
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                self.vision.drawer.draw_landmarks(
                    img,
                    hand_landmarks,
                    self.vision.mp_hands.HAND_CONNECTIONS
                )
                
                lm = hand_landmarks.landmark
                fingers = get_fingers(lm)
                
                x = int(lm[8].x * w)
                y = int(lm[8].y * h)
                
                screen_x = np.interp(x, (100, w - 100), (0, 1920))
                screen_y = np.interp(y, (100, h - 100), (0, 1080))
                
                sx, sy = self.smooth(screen_x, screen_y)
                
                if fingers[1:] == [1, 0, 0, 0]:
                    self.controller.move(sx, sy)
                    current_gesture = "Moving 🖱️"
                    
                elif is_pinch(lm):
                    if config.ENABLE_CLICK:
                        self.controller.click()
                        current_gesture = "Clicking 👆"
                        
                elif fingers[1:] == [0, 0, 0, 0]:
                    if config.ENABLE_DRAG:
                        self.controller.drag(True)
                        current_gesture = "Dragging ✊"
                else:
                    if config.ENABLE_DRAG:
                        self.controller.drag(False)
                        
                if fingers[1:] == [1, 1, 0, 0] and not is_pinch(lm):
                    if config.ENABLE_SCROLL:
                        if y < h/3:
                            self.controller.scroll(1)
                            current_gesture = "Scrolling Up ⬆️"
                        elif y > 2*h/3:
                            self.controller.scroll(-1)
                            current_gesture = "Scrolling Down ⬇️"
                        else:
                            current_gesture = "Scroll Ready ↕️"
                            
                # Overlay stats on the video directly
                cv2.putText(img, f"Gesture: {current_gesture}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (167, 119, 227), 2)
                cv2.putText(img, f"Mouse: {int(sx)}, {int(sy)}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(img, f"Fingers: {fingers}", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.putText(img, f"FPS: {int(fps)}", (w - 150, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")

main_col, side_col = st.columns([3, 1])

with main_col:
    webrtc_streamer(
        key="virtual-mouse",
        video_processor_factory=VideoProcessor,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True
    )

with side_col:
    st.info("💡 **Tip:** Click the 'Start' button inside the video player above. Your camera will stream seamlessly directly to the browser.")
    st.markdown("""
    ### Dashboard Output
    The live stats, FPS, and gesture status are now **drawn directly onto the video feed!**
    
    This completely eliminates UI flickering and provides the smoothest possible real-time web experience.
    """)
