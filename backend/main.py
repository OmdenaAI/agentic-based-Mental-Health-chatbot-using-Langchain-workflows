"""Main module for the FastAPI application."""

# Importing necessary libraries
import os
import torch
import logging
from typing import List
from fastapi import FastAPI
from models import GraphState
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.vectorstores import FAISS
from models import GraphState, SentenceTransformers, TTSInput
from utils import build_lang_graph, store_user_data, create_faiss_db_from_document
from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import soundfile as sf
import numpy as np
import uuid
from kokoro import KPipeline
from pathlib import Path
from fastapi.staticfiles import StaticFiles
import tempfile
import whisper
import io
import numpy as np



logging.basicConfig(logging=logging.INFO)
logger = logging.getLogger(__name__)


os.environ["CUDA_VISIBLE_DEVICES"] = "" #for cuda devices default to cpu
torch.cuda.is_available = lambda: False

app = FastAPI()
storage_path = os.path.join(os.path.dirname(__file__), "storage")
app.mount("/storage", StaticFiles(directory=storage_path), name="storage")
pipeline = KPipeline(lang_code='a')


storage_path =Path(os.getcwd()) / 'storage' 


app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"], #["http://localhost:5173"],  # Frontend url. You can replace the current URL with your frontend URL 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


@app.post("/store/user")
async def store_user_info(state: GraphState) -> list:
    """
    Handles a POST request to stores user data in a JSON file,
    and returns the complete list of all user records.

    This function ensures that user information is persisted between sessions
    by saving User's info into a JSON file (`user.json`). If the file
    doesn't exist, it will be created.
    """
    return store_user_data(state)



@app.post("/chat")
async def chat(state: GraphState):
    """
    Retrieves the query information from the User's message.
    This endpoint is run when the user clicks send, thereby sending the message to this endpoint.
    """

    logger.info(f"state from user: {state}")

    app = build_lang_graph()
    result = app.invoke(state)

    try:
        if result["messages"]:
            reply = result["messages"][-1].content  # Assuming the structure is correct
            logger.info("Reply message relayed")
            logger.info(f"reply: {reply}")
            return {"reply": reply}  # Returning a structured JSON response
        else:
            logger.warning("No response generated")
            return {"reply": "No response generated."}  # Return default message if no messages
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
        
    

@app.post("/create/FAISS")
async def create_faiss_db(
    documents: List[str],
    model_name: SentenceTransformers = SentenceTransformers.ALL_MINILM_L6_V2,
) -> bool:
    """
    Endpoint to create and save a FAISS vector store from a list of input documents.

    Args:
        documents (List[str]): A list of input text documents to be embedded and indexed.
        model_name (SentenceTransformers, optional): The SentenceTransformer model to use
            for generating embeddings. Defaults to ALL_MINILM_L6_V2.

    Returns:
        True if the function runs as expected, False if not
    """
    return create_faiss_db_from_document(documents, model_name.value)




@app.post("/tts")
def generate_speech(data: TTSInput):

    logger.info('#######')
    logger.info('#######')
    logger.info('#######')
    logger.info('#######')
    logger.info('#######')
    logger.info(f"{data.text}")
    audio_chunks = []

    for _, _, audio in pipeline(data.text, voice="af_heart"):
        audio_chunks.append(audio)

    if not audio_chunks:
        raise HTTPException(status_code=500, detail="No audio generated")

    audio = np.concatenate(audio_chunks)
    file_id = uuid.uuid4().hex
    filename = f"{storage_path}/{file_id}.wav"
    sf.write(filename, audio, 24000)

    return {'id': file_id}




@app.post('/store/audio')
async def store_user_audio(audio: UploadFile=File(...)):
    """
        Stores the audio from the user to a file in the backend and returns text to the frontend
    """


    # storing audio
    try:
        os.makedirs("storage", exist_ok=True)
        filepath = storage_path / audio.filename
        print(f"filepath: {filepath}")
        with open(filepath, "wb") as f:
            f.write(await audio.read())
        
        # Transcribe
        whisper_model = whisper.load_model("base")
        result = whisper_model.transcribe(str(filepath))
        print(f"text from whishper:{result['text']}")
        return {"text_from_audio": result["text"]}

    except Exception as e:
        print("Exception occurred:", e)
        return JSONResponse(status_code=500, content={"error": str(e)})

