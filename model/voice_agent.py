import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()

def listen_from_mic():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand you."
        except sr.RequestError:
            return "Speech recognition service is unavailable."

def speak_response(response_text):
    tts_engine = pyttsx3.init()
    tts_engine.say(response_text)
    tts_engine.runAndWait()
    tts_engine.stop()