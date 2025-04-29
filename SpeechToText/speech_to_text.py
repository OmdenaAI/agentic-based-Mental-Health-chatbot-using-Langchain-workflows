# -*- coding: utf-8 -*-

# !pip install -q SpeechRecognition

import speech_recognition as sr

import IPython.display as ipd

# Load your audio file
audio_file = "/content/drive/MyDrive/Audios/20250416_160117.m4a" #"/content/drive/MyDrive/chunk_2.wav"  # Replace with your actual audio file

ipd.Audio("/content/drive/MyDrive/chunk_2.wav")

# Initialize the recognizer
recognizer = sr.Recognizer()

# Use the audio file as input
with sr.AudioFile(audio_file) as source:
    print("Listening...")
    audio_data = recognizer.record(source)

# Recognize speech and convert it to text
try:
    text = recognizer.recognize_google(audio_data)
    print("Text from audio:")
    print(text)
except sr.UnknownValueError:
    print("Sorry, the audio was not clear enough to understand.")
except sr.RequestError as e:
    print(f"Could not request results from the speech recognition service; {e}")

