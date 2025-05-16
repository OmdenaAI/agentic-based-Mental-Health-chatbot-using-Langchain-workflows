import pyttsx3

engine = pyttsx3.init(driverName='sapi5')  # force Windows voice engine
voices = engine.getProperty('voices')

for i, voice in enumerate(voices):
    print(f"{i}: {voice.name} ({voice.id})")
