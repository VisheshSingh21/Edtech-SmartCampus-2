import streamlit as st
import plotly.express as px
import pandas as pd
import random
import time

# -----------------------------------
# ⚙️ Basic Config
# -----------------------------------
st.set_page_config(
    page_title="EduPulse — Smart Classroom Engagement System",
    page_icon="🎓",
    layout="wide",
)

# Sidebar Navigation
st.sidebar.title("EduPulse 🎓")
st.sidebar.markdown("### Smart Classroom Engagement System")
page = st.sidebar.radio(
    "Navigate",
    [
        "🧠 Emotion Detection",
        
        "💬 Engagement Analysis",
        
        "📊 Teacher Dashboard",
        
        "🗣 Voice Feedback",
        
        "🧾 Summary Report",
        
        "⚙ Settings",
    ],
)

# -----------------------------------
# 🧠 Emotion Detection Page
# -----------------------------------
if page == "🧠 Emotion Detection":
    st.title("🧠 Real-time Emotion Detection")

    st.write("System captures student facial expressions and detects emotions in real time.")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.image("https://cdn.pixabay.com/photo/2016/03/31/19/57/avatar-1295390_1280.png", caption="Live Camera Feed (Mock)")

    with col2:
        emotion = random.choice(["😊 Happy", "😐 Neutral", "😕 Confused", "😞 Sad", "🥱 Bored"])
        confidence = random.randint(70, 98)
        st.metric("Detected Emotion", emotion)
        st.metric("Confidence", f"{confidence}%")

    st.info("Note: In full version, webcam and FER/DeepFace model will be used for live detection.")

# -----------------------------------
# 💬 Engagement Analysis Page
# -----------------------------------
elif page == "💬 Engagement Analysis":
    st.title("💬 Engagement Analysis")
    st.write("Track student engagement levels over time.")

    # Simulated engagement data
    times = [f"10:{i:02d}" for i in range(1, 11)]
    scores = [random.randint(40, 90) for _ in range(10)]
    emotions = ["Happy", "Neutral", "Confused", "Bored", "Sad"]

    # Charts
    fig1 = px.line(
        x=times,
        y=scores,
        title="📈 Engagement Trend (Last 10 Minutes)",
        labels={"x": "Time", "y": "Engagement Score"},
    )

    fig2 = px.pie(
        names=emotions,
        values=[random.randint(5, 40) for _ in emotions],
        title="🎭 Emotion Distribution",
    )

    col1, col2 = st.columns(2)
    col1.plotly_chart(fig1, use_container_width=True)
    col2.plotly_chart(fig2, use_container_width=True)

    avg = sum(scores) // len(scores)
    st.metric("Average Engagement", f"{avg}%")

# -----------------------------------
# 📊 Teacher Dashboard Page
# -----------------------------------
elif page == "📊 Teacher Dashboard":
    st.title("📊 Teacher Dashboard")
    st.write("Monitor class engagement, emotions, and alerts in real time.")

    # Simulated metrics
    engagement_score = random.randint(35, 95)
    st.metric("Current Engagement Score", f"{engagement_score}%")

    # Engagement status feedback
    if engagement_score > 70:
        st.success("🟢 Students are highly engaged! Great job!")
    elif 50 <= engagement_score <= 70:
        st.warning("🟡 Engagement moderate — consider adding short Q&A.")
    else:
        st.error("🔴 Engagement low — students may be distracted. Try an activity!")

    st.subheader("Emotion Heatmap (Sample Data)")
    df = pd.DataFrame({
        "Student": [f"Student {i}" for i in range(1, 11)],
        "Happy": [random.randint(0, 10) for _ in range(10)],
        "Confused": [random.randint(0, 10) for _ in range(10)],
        "Bored": [random.randint(0, 10) for _ in range(10)],
    })
    fig = px.imshow(df.set_index("Student").T, text_auto=True, color_continuous_scale="RdYlGn")
    st.plotly_chart(fig, use_container_width=True)

    st.info("Alerts will appear here when engagement drops or student voice is missing.")

# -----------------------------------
# 🗣 Voice Feedback Page
# -----------------------------------
elif page == "🗣 Voice Feedback":
    st.title("🗣 Student Voice Feedback")
    st.write("System listens for student responses when teacher asks a question.")

    start = st.button("🎤 Start Listening")

    if start:
        with st.spinner("Listening for student response (10 seconds)..."):
            time.sleep(3)
            voice_detected = random.choice([True, False])

        if voice_detected:
            st.success("🎧 Voice detected — student answered.")
        else:
            st.error("⚠ No voice detected — feedback sent to teacher dashboard.")

    st.caption("Powered by SpeechRecognition + PyAudio (in full version).")

# -----------------------------------
# 🧾 Summary Report Page
# -----------------------------------
elif page == "🧾 Summary Report":
    st.title("🧾 Class Summary Report")
    st.write("View and download session summary after class.")

    avg_engagement = random.randint(60, 90)
    st.metric("Average Engagement", f"{avg_engagement}%")

    emotion_summary = pd.DataFrame({
        "Emotion": ["Happy", "Neutral", "Confused", "Bored", "Sad"],
        "Count": [random.randint(5, 25) for _ in range(5)]
    })

    st.bar_chart(emotion_summary.set_index("Emotion"))

    if st.button("📄 Generate PDF Report"):
        st.success("✅ Report generated and saved locally as `class_summary.pdf` (mock).")

# -----------------------------------
# ⚙ Settings Page
# -----------------------------------
elif page == "⚙ Settings":
    st.title("⚙ Settings")
    st.write("Customize EduPulse settings for your classroom.")

    lang = st.selectbox("🌐 Choose Language", ["English", "Hindi"])
    threshold = st.slider("🎯 Engagement Alert Threshold", 0, 100, 50)
    st.file_uploader("🔊 Upload Custom Alert Sound (optional)", type=["mp3", "wav"])

    st.info(f"Language set to {lang}, alert threshold = {threshold}%")
    st.caption("All changes saved locally.")
