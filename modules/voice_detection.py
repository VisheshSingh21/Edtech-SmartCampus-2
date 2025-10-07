import speech_recognition as sr
import time

def listen_for_answer(timeout=10):
    """Listens to student's response for given timeout"""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("🎤 Listening for student's answer...")
        recognizer.adjust_for_ambient_noise(source)
        audio = None
        try:
            audio = recognizer.listen(source, timeout=timeout)
        except sr.WaitTimeoutError:
            print("⏱️ No voice detected within time window.")
            return {"status": "no_voice", "text": None}

    try:
        text = recognizer.recognize_google(audio)
        print(f"🗣️ Student said: {text}")
        return {"status": "voice_detected", "text": text}
    except sr.UnknownValueError:
        print("❌ Voice detected but not recognized as answer.")
        return {"status": "unrecognized", "text": None}
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return {"status": "error", "text": None}
