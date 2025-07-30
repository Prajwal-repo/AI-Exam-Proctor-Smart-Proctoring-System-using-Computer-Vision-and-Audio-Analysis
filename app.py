import streamlit as st
import cv2
from utils.webcam import get_frame
from utils.visibility import is_dark
from utils.detect_objects import detect_objects
from utils.voice_alert import is_voice_detected

st.set_page_config(page_title="AI Proctoring System", layout="wide")
st.title("🎓 AI Exam Proctoring System")

# Initialize session state
if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False

col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Start Monitoring"):
        st.session_state.monitoring = True

with col2:
    if st.button("⏹️ Stop Monitoring"):
        st.session_state.monitoring = False

frame_placeholder = st.empty()
alert_placeholder = st.empty()

# Monitoring loop
if st.session_state.monitoring:
    while st.session_state.monitoring:
        frame = get_frame()
        if frame is None:
            st.warning("Camera not available.")
            break

        # Process checks
        dark = is_dark(frame)
        objects = detect_objects(frame)
        voice = is_voice_detected()

        # Display frame
        frame_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")

        # Show alerts
        alerts = []
        if dark:
            alerts.append("🔦 Low lighting detected")
        if objects:
            alerts.append(f"📱 Suspicious object(s): {', '.join(objects)}")
        if voice:
            alerts.append("🎤 Voice activity detected")

        if alerts:
            alert_placeholder.warning(" | ".join(alerts))
        else:
            alert_placeholder.success("✅ All clear")

        # Break condition to stop loop via UI
        if not st.session_state.monitoring:
            break
