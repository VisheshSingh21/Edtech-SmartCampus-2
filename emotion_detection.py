import cv2
from fer import FER

cap = cv2.VideoCapture(0)  # Webcam
detector = FER(mtcnn=True)  # Face + emotion detection

while True:
    ret, frame = cap.read()
    if not ret:
        break

    result = detector.detect_emotions(frame)
    if result:
        emotions = result[0]["emotions"]
        print(emotions)  # {"happy": 0.8, "sad": 0.1,...}

    cv2.imshow("EduPulse Emotion Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()