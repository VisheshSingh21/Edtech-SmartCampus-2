from deepface import DeepFace
import cv2
import pandas as pd
import time
import os

# Create data folder if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# CSV file to store emotion data
emotion_file = "data/emotions.csv"

# If file doesn't exist, create it with headers
if not os.path.exists(emotion_file):
    df = pd.DataFrame(columns=["timestamp", "emotion"])
    df.to_csv(emotion_file, index=False)

# Start webcam
cap = cv2.VideoCapture(0)

print("Starting Emotion Detection. Press 'q' to stop.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{timestamp} → Emotion: {emotion}")

        # Append emotion data to CSV
        df = pd.DataFrame([[timestamp, emotion]], columns=["timestamp", "emotion"])
        df.to_csv(emotion_file, mode='a', header=False, index=False)

        # Display emotion on frame
        cv2.putText(frame, emotion, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    except Exception as e:
        print("Error:", e)

    # Show webcam feed
    cv2.imshow("EduPulse Emotion Detection", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()