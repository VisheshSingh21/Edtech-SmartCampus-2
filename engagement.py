import pandas as pd
import time
import os

# Paths
emotion_file = "data/emotions.csv"
engagement_file = "data/engagement.csv"

# Create engagement file if not exists
if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(engagement_file):
    df = pd.DataFrame(columns=["timestamp", "engagement_score"])
    df.to_csv(engagement_file, index=False)

# Emotion weights
weights = {
    "happy": 2,
    "neutral": 1,
    "sad": -1,
    "bored": -2,
    "angry": -2,
    "surprise": 1,
    "fear": -1,
    "disgust": -2
}

print("Starting Engagement Calculation... Press CTRL+C to stop.")

try:
    while True:
        if os.path.exists(emotion_file):
            df = pd.read_csv(emotion_file)

            # Last 30 seconds of data
            cutoff = pd.Timestamp.now() - pd.Timedelta(seconds=30)
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
            recent = df[df["timestamp"] >= cutoff]

            if not recent.empty:
                # Calculate weighted score
                score = sum(weights.get(emotion, 0) for emotion in recent["emotion"]) / len(recent)
                score = max(min(score * 25, 100), 0)  # scale to 0–100

                timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{timestamp} → Engagement Score: {score:.2f}")

                # Append to engagement file
                pd.DataFrame([[timestamp, score]], columns=["timestamp", "engagement_score"]).to_csv(
                    engagement_file, mode="a", header=False, index=False
                )

        time.sleep(30)  # repeat every 30 seconds

except KeyboardInterrupt:
    print("Engagement calculation stopped.")