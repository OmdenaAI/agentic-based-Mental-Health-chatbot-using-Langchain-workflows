# fastapi_app/main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import whisper
import requests
import json
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import os
import pyttsx3
from tempfile import NamedTemporaryFile
from fastapi.responses import FileResponse
import uuid
from mentalhealth_chatbot.main import get_crew_response  # ✅ Use CrewAI






# --- Setup ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- LLM and STT Setup ---
ollama_url = "http://localhost:11434/api/generate"  # Ollama server
whisper_model = whisper.load_model("base")  # Whisper for STT

# --- Embeddings setup ---
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = None

# Create dummy vector store
texts = ["Take a deep breath and relax.", "Try journaling your thoughts.", "Go for a short walk outside."]
docs = [Document(page_content=t) for t in texts]
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
chunks = text_splitter.split_documents(docs)
vector_store = FAISS.from_documents(chunks, embedding_model)

# --- Pydantic schemas ---
class ChatRequest(BaseModel):
    message: str
    history: List[str] = []

# --- Routes ---
"""@app.post("/chat")
def chat(req: ChatRequest):
    prompt = "\n".join(req.history + [f"User: {req.message}", "Bot:"])
    response = requests.post(ollama_url, json={"model": "mistral", "prompt": prompt}, stream=True)

    print("=== RAW STREAMED RESPONSE ===")
    full_stream = b""
    for line in response.iter_lines():
        print(line)  # <-- Add this to see each line
        full_stream += line + b"\n"

    try:
        all_lines = full_stream.decode("utf-8").split("\n")
        last_valid = ""
        for l in all_lines:
            if l.strip():
                parsed = json.loads(l)
                if "response" in parsed:
                    last_valid += parsed["response"]
        bot_reply = last_valid.strip()
    except Exception as e:
        print(f"Parsing error: {e}")
        bot_reply = "Sorry, I couldn't respond."

    return {"response": bot_reply}
"""
"""@app.post("/chat")
def chat(req: ChatRequest):
    try:
        bot_reply = get_crew_response(req.message)
        bot_reply = bot_reply.replace("(Tip 1 from doc1)", "").replace("(Tip 2 from doc2)", "")
    except Exception as e:
        print(f"[Crew Error] {e}")
        bot_reply = "Sorry, I couldn't respond."

    return {"response": bot_reply}
    """
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        result = get_crew_response(req.message)
        if hasattr(result, "output"):
            bot_reply = result.output
        else:
            bot_reply = str(result)

        # Optional: clean up unwanted tags from tips (if present)
        bot_reply = bot_reply.replace("(Tip 1 from doc1)", "").replace("(Tip 2 from doc2)", "")
    except Exception as e:
        print(f"[Crew Error] {e}")
        bot_reply = "Sorry, I couldn't respond."

    return {"response": bot_reply}

@app.post("/transcribe")
def transcribe_audio(file: UploadFile = File(...)):
    audio_path = f"temp_audio.wav"
    with open(audio_path, "wb") as f:
        f.write(file.file.read())
    result = whisper_model.transcribe(audio_path)
    os.remove(audio_path)
    return {"transcript": result["text"]}

@app.get("/retrieve")
def retrieve_tips(query: str):
    results = vector_store.similarity_search(query, k=2)
    tips = [doc.page_content for doc in results]
    return {"tips": tips}




@app.post("/speak")
def text_to_speech(text: str):
    # Generate a unique filename
    filename = f"speech_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join("temp_audio", filename)

    # Ensure the directory exists
    os.makedirs("temp_audio", exist_ok=True)

    # Init engine and save audio
    engine = pyttsx3.init()
    engine.save_to_file(text, filepath)
    engine.runAndWait()

    # Check if file was created
    if not os.path.exists(filepath):
        return {"error": "Failed to generate speech file."}

    return FileResponse(
        path=filepath,
        media_type="audio/mpeg",
        filename=filename
    )
