import streamlit as st
import plotly.express as px
import pandas as pd
import random
import time
import json
import os
import speech_recognition as sr



# -------------------------------
# Load language file
# -------------------------------
def load_language(lang_code):
    with open(f"languages/{lang_code}.json", "r", encoding="utf-8") as f:
        return json.load(f)

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(page_title="EduPulse", page_icon="🎓", layout="wide")

# Sidebar language selection
lang_choice = st.sidebar.selectbox("🌐 Choose Language / भाषा चुनें", ["English", "Hindi"])
lang_code = "en" if lang_choice == "English" else "hi"
L = load_language(lang_code)

# Sidebar Navigation
st.sidebar.title(L["sidebar_title"])
st.sidebar.markdown(f"### {L['sidebar_desc']}")
page = st.sidebar.radio(
    "Navigate",
    [
        L["emotion_detection"],
        L["engagement_analysis"],
        L["student_dashboard"], 
        L["teacher_dashboard"],
        L["voice_feedback"],
        L["summary_report"],
        L["settings"],
    ],
)

# -----------------------------------
# 🧠 Emotion Detection Page
# -----------------------------------
if page == L["emotion_detection"]:
    st.title(L["emotion_detection"])
    st.write(L["note"])
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Streamlit device camera input
        camera_image = st.camera_input("📷 Live Camera Feed")

    with col2:
        # Sample random emotion metrics
        emotion = random.choice(["😊 Happy", "😐 Neutral", "😕 Confused", "😞 Sad", "🥱 Bored"])
        confidence = random.randint(70, 98)
        st.metric(L["detected_emotion"], emotion)
        st.metric(L["confidence"], f"{confidence}%")

# -----------------------------------
# 💬 Engagement Analysis Page
# -----------------------------------
elif page == L["engagement_analysis"]:
    st.title(L["engagement_analysis"])
    st.write("Track student engagement levels over time.")  # Can translate later if needed
    times = [f"10:{i:02d}" for i in range(1, 11)]
    scores = [random.randint(40, 90) for _ in range(10)]
    emotions = ["Happy", "Neutral", "Confused", "Bored", "Sad"]

    fig1 = px.line(x=times, y=scores, title="📈 Engagement Trend (Last 10 Minutes)", labels={"x": "Time", "y": "Engagement Score"})
    fig2 = px.pie(names=emotions, values=[random.randint(5, 40) for _ in emotions], title="🎭 Emotion Distribution")
    col1, col2 = st.columns(2)
    col1.plotly_chart(fig1, use_container_width=True)
    col2.plotly_chart(fig2, use_container_width=True)
    avg = sum(scores) // len(scores)
    st.metric(L["avg_engagement"], f"{avg}%")

# -----------------------------------
# 🎓 Student Dashboard (NEW PAGE)
# -----------------------------------
if page == L["student_dashboard"]:
    st.title(L["student_dashboard"])
    st.markdown("Welcome to your learning area! 🎥 Watch your offline recorded lectures below.")

    video_folder = r"C:\Users\VisheshSingh\Downloads"
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)
        st.warning("📁 'videos' folder created. Please add some .mp4 lecture videos inside it.")
    else:
        videos = [f for f in os.listdir(video_folder) if f.endswith(".mp4")]
        if videos:
            selected_video = st.selectbox("Select a Lecture", videos)
            video_path = os.path.join(video_folder, selected_video)
            st.video(video_path)
            st.success(f"Now playing: {selected_video}")
        else:
            st.info("No video lectures found. Please add some `.mp4` files to the `videos/` folder.")

# -----------------------------------
# 📊 Teacher Dashboard Page
# -----------------------------------
elif page == L["teacher_dashboard"]:
    st.title(L["teacher_dashboard"])
    st.write(L["monitor_class"])
    engagement_score = random.randint(35, 95)
    st.metric(L["avg_engagement"], f"{engagement_score}%")
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
    st.info(L["alerts_info"])

# -----------------------------------
# 🗣 Voice Feedback Page
# -----------------------------------
elif page == L["voice_feedback"]:
    st.title(L["voice_feedback"])
    
    # Choose translation target
    target_lang = st.radio("Translate Speech to:", ["English", "Hindi"])
    target_code = "en" if target_lang == "English" else "hi"
    
    start = st.button(L["start_listening"])
    
    if start:
        with st.spinner("Listening for student response (10 seconds)..."):
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                try:
                    audio = recognizer.listen(source, timeout=10)
                    text = recognizer.recognize_google(audio)
                    st.info(f"🎙 Original: {text}")
                    
                    translated_text = translate_text(text, target_code)
                    st.success(f"🌐 Translated ({target_lang}): {translated_text}")
                except sr.WaitTimeoutError:
                    st.error("⚠ No voice detected — feedback sent to teacher dashboard.")
                except sr.UnknownValueError:
                    st.error("⚠ Could not understand speech — feedback sent to teacher dashboard.")
                except Exception as e:
                    st.error(f"⚠ Error: {e}")


# -----------------------------------
# 🧾 Summary Report Page
# -----------------------------------
elif page == L["summary_report"]:
    st.title(L["summary_report"])
    st.write(L["view_download_summary"])
    avg_engagement = random.randint(60, 90)
    st.metric(L["avg_engagement"], f"{avg_engagement}%")
    emotion_summary = pd.DataFrame({
        "Emotion": ["Happy", "Neutral", "Confused", "Bored", "Sad"],
        "Count": [random.randint(5, 25) for _ in range(5)]
    })
    st.bar_chart(emotion_summary.set_index("Emotion"))
    if st.button(L["generate_pdf"]):
        st.success(L["report_generated"])

# -----------------------------------
# ⚙ Settings Page
# -----------------------------------
elif page == L["settings"]:
    st.title(L["settings"])
    lang = st.selectbox(L["choose_language"], ["English", "Hindi"])
    threshold = st.slider(L["alert_threshold"], 0, 100, 50)
    st.file_uploader(L["upload_sound"], type=["mp4", "wav"])
    st.info(f"Language set to {lang}, alert threshold = {threshold}%")
    st.caption("All changes saved locally.")