# -*- coding: utf-8 -*-

# !pip install -q SpeechRecognition

import speech_recognition as sr

import IPython.display as ipd

# Load your audio file
# audio_file = "audio.wav"  # Replace with your actual audio file

def speech_to_text(audio_file):
    """
    Convert speech in an audio file to text using Google Web Speech API.
    
    Parameters:
    audio_file (str): Path to the audio file.
    
    Returns:
    str: Recognized text from the audio.
    """
    # Load the audio file
    # ipd.Audio(audio_file)

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

if __name__ == "__main__":
    # Example usage
    print("main function")
    audio_file = "audio.wav"  # Replace with your actual audio file
    speech_to_text(audio_file)
