import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel
from chatbot import get_response

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    history: list[str] = []


@app.get("/")
def root():
    return {"message": "FastAPI is running"}


@app.post("/chat")
def chat_endpoint(chat: ChatRequest):
    response = get_response(chat.message, chat.history)
    return {"response": response}

