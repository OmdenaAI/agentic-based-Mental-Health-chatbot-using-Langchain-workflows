from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import whisper
import uuid
import os
import pyttsx3
from tempfile import NamedTemporaryFile
from langchain.memory import ConversationBufferMemory
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from mentalhealth_chatbot.main import get_crew_response  # ✅ Use CrewAI

# --- Memory Setup ---
memory = ConversationBufferMemory(return_messages=True)

# --- FastAPI Setup ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Serve audio files ---
app.mount("/audio", StaticFiles(directory="temp_audio"), name="audio")

# --- STT & Embedding Setup ---
whisper_model = whisper.load_model("base")
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# --- Dummy Vector Store Setup ---
texts = ["Take a deep breath and relax.", "Try journaling your thoughts.", "Go for a short walk outside."]
docs = [Document(page_content=t) for t in texts]
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
chunks = text_splitter.split_documents(docs)
vector_store = FAISS.from_documents(chunks, embedding_model)

# --- Request Schema ---
class ChatRequest(BaseModel):
    message: str
    history: List[str] = []
    mode: str = "text"  # text or voice

# --- Chat Endpoint ---
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        context = memory.load_memory_variables({})
        history = context.get("history", "")
        full_input = f"{history}\nUser: {req.message}"

        result = get_crew_response(full_input)
        bot_reply = result.output if hasattr(result, "output") else str(result)
        bot_reply = bot_reply.replace("(Tip 1 from doc1)", "").replace("(Tip 2 from doc2)", "")

        memory.save_context({"input": req.message}, {"output": bot_reply})

        # If voice mode, generate audio file
        if req.mode == "voice":
            filename = f"speech_{uuid.uuid4().hex}.mp3"
            filepath = os.path.join("temp_audio", filename)
            os.makedirs("temp_audio", exist_ok=True)
            engine = pyttsx3.init()
            engine.save_to_file(bot_reply, filepath)
            engine.runAndWait()

            return {"response": bot_reply, "audio": f"/audio/{filename}"}

        return {"response": bot_reply}

    except Exception as e:
        print(f"[Crew Error] {e}")
        return {"response": "Sorry, I couldn't respond."}

# --- STT Endpoint ---
@app.post("/transcribe")
def transcribe_audio(file: UploadFile = File(...)):
    audio_path = "temp_audio.wav"
    with open(audio_path, "wb") as f:
        f.write(file.file.read())
    result = whisper_model.transcribe(audio_path)
    os.remove(audio_path)
    return {"transcript": result["text"]}

# --- RAG Tip Retrieval ---
@app.get("/retrieve")
def retrieve_tips(query: str):
    results = vector_store.similarity_search(query, k=2)
    tips = [doc.page_content for doc in results]
    return {"tips": tips}

# --- Manual TTS Endpoint ---
@app.post("/speak")
def text_to_speech(text: str):
    filename = f"speech_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join("temp_audio", filename)
    os.makedirs("temp_audio", exist_ok=True)
    engine = pyttsx3.init()
    engine.save_to_file(text, filepath)
    engine.runAndWait()
    if not os.path.exists(filepath):
        return {"error": "Failed to generate speech file."}
    return FileResponse(path=filepath, media_type="audio/mpeg", filename=filename)
