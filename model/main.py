from fastapi import FastAPI
from pydantic import BaseModel
from voice_agent import listen_from_mic, speak_response
from autogen_LlamaIndex import handle_user_query
from logger import log_conversation

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/speech-to-text")
def speech_to_text():
    text = listen_from_mic()
    return {"transcription": text}

@app.post("/text-to-speech")
def text_to_speech(data: TextInput):
    speak_response(data.text)
    return {"status": "spoken"}

@app.post("/chat")
def chat(data: TextInput):
    try:
        user_query = data.text
        bot_response = handle_user_query(user_query)
        log_conversation(user_query, bot_response)
        return {"response": bot_response}
    except Exception as e:
        print(f"[ERROR] Chat processing failed: {e}")
        return {"error": str(e)}

