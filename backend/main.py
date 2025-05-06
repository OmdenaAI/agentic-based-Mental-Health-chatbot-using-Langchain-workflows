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
from models import GraphState, SentenceTransformers
from utils import build_lang_graph, store_user_data, create_faiss_db_from_document


logging.basicConfig(logging=logging.INFO)
logger = logging.getLogger(__name__)


os.environ["CUDA_VISIBLE_DEVICES"] = "" #for cuda devices default to cpu
torch.cuda.is_available = lambda: False

app = FastAPI()

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
