import os
import json
import logging
from glob import glob
from sys import exception
from typing import List
from pathlib import Path

from torch import device

from torch import embedding
from base_context import base_context
from langgraph.graph import StateGraph

from langchain_core.messages import AIMessage
from langchain_community.vectorstores import FAISS
from models import GraphState, SentenceTransformers
from langchain_core.runnables import RunnableLambda
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableLambda




# configure logging settings
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# get google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def store_user_data(state: GraphState):
    """
    Stores user data from the given GraphState into a JSON file.

    This function serializes the `state` object using `model_dump()` and appends
    it to a list of previous user interactions stored in `user.json`. If the file
    doesn't exist or contains invalid data, a new list is created. The updated
    list is saved back to the same file.

    Parameters:
        state (GraphState): The current user's session data.

    Returns:
        list: A list of all user session records including the newly added one.
    """

    user_info_path = Path(os.getcwd()) / "storage"
    os.makedirs(user_info_path, exist_ok=True)

    user_file = user_info_path / "user.json"
    current_user_info = state.model_dump()

    # Load existing data if file exists, otherwise start with empty list
    if user_file.exists():
        with open(user_file, "r") as file:
            try:
                all_users_info = json.load(file)
                if not isinstance(all_users_info, list):
                    all_users_info = []
            except json.JSONDecodeError:
                all_users_info = []
    else:
        all_users_info = []

    length_before = len(all_users_info)  # length of user profiles before update

    all_users_info.append(
        current_user_info
    )  # append current_user_info to all_user_info

    length_after = len(all_users_info)  # length of user profiles after update

    logger.info(f"length of all user profiles: {len(all_users_info)}")

    with open(user_file, "w") as file:  # update the file
        json.dump(all_users_info, file, indent=2)

    # checking if Users info file was updated with current User info
    if length_before != length_after:
        logging.info("New User info was added")
    else:
        logging.error("Users info file is not updated with current User info")

    return all_users_info


def create_faiss_db_from_document(documents: List[str], model_name) -> bool:
    print(f"{model_name=}")
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=10)
    split_docs = splitter.create_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    vector_store = FAISS.from_documents(split_docs, embeddings)
    vector_store.save_local("storage/")  # store to storage folder

    # check if the faiss documents were saved to folder - a .faiss and .pkl file should exist in the folder
    storage = Path(os.getcwd()) / "storage"
    faiss_exists = any(storage.glob("*.faiss"))
    pkl_exists = any(storage.glob("*.pkl"))
    if faiss_exists and pkl_exists:
        logger.info("FAISS vector store created and saved")
        return True
    else:
        logger.error(
            "FAISS vector was not created, possibly due to missing or invalid input documents."
        )
        return False


def retrieve_faiss_db(
    storage: str | Path,
    model_name: SentenceTransformers = SentenceTransformers.ALL_MINILM_L6_V2,
) -> FAISS:
    """
    Loads a FAISS vector store from the specified local storage path using the provided embedding model.

    Args:
        storage (str | Path): Path to the local FAISS index directory.
        model_name (SentenceTransformers, optional): Enum value representing the name of the sentence-transformers model to use for embeddings.

    Returns:
        FAISS: The loaded FAISS vector store object.

    Raises:
        ValueError: If the storage path is not provided or the FAISS index could not be loaded.
        Exception: For any other unexpected errors during loading.
    """
    if storage:
        try:
            # model = SentenceTransformer(model_name_or_path=model_name.value, device="cpu")
            embeddings = HuggingFaceEmbeddings(model_name=model_name.value, model_kwargs = {'device': 'cpu'})
            logger.info('#########################')
            logger.info('before loading faiss load local')
            retrieved_faiss_db = FAISS.load_local(
                storage, embeddings, allow_dangerous_deserialization=True
            )
            logger.info('#########################')
            logger.info('after loading faiss load local')


            if retrieved_faiss_db:
                logger.info(
                    f"FAISS DB successfully retrieved from {storage}. Proceeding with the next steps."
                )
                return retrieved_faiss_db
            else:
                msg = f"FAISS DB is empty or failed to load from {storage}."
                logger.error(msg)
                raise ValueError(msg)
        except Exception as e:
            logger.error(
                f"Error: {e}. "
                "Ensure the file exists and the path is correct."
            )
            raise
    else:
        msg = "No storage path provided for FAISS DB."
        logger.error(msg)
        raise ValueError(msg)


def retrieve_relevant_docs(
    state: GraphState,
    storage: str | Path = Path(os.getcwd()) / 'storage',
    model_name: SentenceTransformers = SentenceTransformers.ALL_MINILM_L6_V2,
) -> GraphState:
    """
    Retrieves relevant documents from a FAISS vector store based on the user's query
    and updates the GraphState with those documents.

    Args:
        state (GraphState): The current state of the conversation containing the user's query.
        storage (str | Path): Path to the local FAISS vector store.
        model_name (SentenceTransformers, optional): The embedding model to use for retrieval.

    Returns:
        GraphState: Updated state with relevant documents added to the "docs" field.
    """
    faiss_db = retrieve_faiss_db(storage, model_name)
    vector_retriever = faiss_db.as_retriever()
    logger.info(f'Query: {state.query}')

    try:
        relevant_docs = vector_retriever.invoke(state.query)
        if relevant_docs:
            state.docs = relevant_docs
            logger.info(
                f"Retrieved {len(relevant_docs)} documents for query: {state.query}"
            )
        else:
            state.docs = []
            logger.warning(f"No relevant documents found for query: {state.query}")
    except Exception as e:
        logger.error(f"Error during document retrieval: {e}")
        raise e

    return state


def initialize_LLM(
    model: str = "gemini-1.5-flash", temperature: int = 0, google_api_key: str = None
) -> ChatGoogleGenerativeAI:
    """
    Initializes and returns a ChatGoogleGenerativeAI LLM with the specified parameters.

    Args:
        model (str): The model name to use. Default is "gemini-1.5-flash".
        temperature (int): Sampling temperature for response randomness. Default is 0 (deterministic).
        google_api_key (str): Your Google API key for authentication.

    Returns:
        ChatGoogleGenerativeAI: An instance of the initialized LLM.

    Raises:
        ValueError: If the API key is missing or empty.
        Exception: If initialization of the LLM fails for any reason.
    """
    if not google_api_key:
        raise ValueError("Google API key is required to initialize the LLM.")

    try:
        llm = ChatGoogleGenerativeAI(
            model=model, temperature=temperature, google_api_key=google_api_key
        )
        logger.info("LLM initialised successfully")
        return llm

    except Exception as e:
        raise RuntimeError(f"Failed to initialize LLM: {e}")


def rewrite_reply(state: GraphState, llm:ChatGoogleGenerativeAI) -> GraphState:
    """
    Rewrites the last AI-generated message in the conversation to better align with the user's emotional state.

    This function takes the most recent reply in the conversation state, generates a prompt to rewrite it with greater emotional relevance, 
    and uses the provided language model (LLM) to create the revised message. If the rewrite fails, a fallback message is appended. 
    The updated message is appended to the conversation, and the conversation state is returned with `state["next"]` set to "relevant".

    Args:
        state (GraphState): The current state of the conversation, including messages and user emotion.
        llm (ChatGoogleGenerativeAI): An instance of the language model used to perform the rewrite.

    Returns:
        GraphState: The updated conversation state with the rewritten message.
    """

    previous_reply = state.messages[-1].content
    prompt = f"Rewrite this reply to be more aligned with the user's emotional state ({state.emotion}): {previous_reply}"
    try:
        response = llm.invoke(prompt)
        reply = response.content if hasattr(response, "content") else response
        state.messages.append(AIMessage(content=reply))
        logger.info("Rewrote response successfully")
    except Exception as e:
        logger.error(f"Failed to rewrite response: {str(e)}")
        reply = "I'm sorry, I couldn't rewrite the response. Please try again."
        state.messages.append(AIMessage(content=reply))
    
    state.next = "END"
    return state


def generate_response(state: GraphState) -> GraphState:
    """
    Generates a response from the LLM based on user input and retrieved documents.

    Constructs a prompt using the user's demographic and emotional state, along with the 
    base context and retrieved documents. Sends the prompt to the LLM, processes the 
    response, and updates the conversation state with the reply. Also determines the 
    relevance of the response content to guide the next step in the flow.

    Args:
        state (GraphState): The current state containing user input, context, and retrieved docs.

    Returns:
        GraphState: The updated state including the generated message and next flow decision.
    """

    # initialize LLM
    llm = initialize_LLM(google_api_key=GOOGLE_API_KEY)

    # initialize Prompt
    prompt = (
        f"User (Age: {state.age}, Gender: {state.gender}, Emotion: {state.emotion}): {state.query}\n"
        f"{base_context}. Generate a response like a message conversation between two friends of at most two sentences based on all the instructions in the base context with the information in {state.docs}."
        f"The response must incorporate relevant suggestions from the retrieved documents, especially from the mental health dataset, when applicable."
    )

    # Add Language capabilities
    language = state.language
    if language.lower() != 'english':
        prompt += f"Translate the final answer to {language}."

    # invoke llm
    try:
        # Invoke the LLM with the prompt
        response = llm.invoke(prompt)
        reply = response.content if hasattr(response, "content") else response

        # Check if the reply contains any meaningful content
        if reply.strip():  # strip() removes leading and trailing whitespace
            state.messages.append(AIMessage(content=reply))
            logger.info("Generated a valid response.")
        else:
            # Log and provide a fallback for empty or whitespace-only response
            logger.warning("Generated an empty or whitespace-only response.")
            reply = "I'm sorry, I couldn't generate a response. Please try again."
            state.messages.append(AIMessage(content=reply))
    except Exception as e:
        # Handle and raise exceptions
        logger.error(f"Error generating response: {e}")
        raise e  # Re-raise the exception after logging it

    # Check if the response contains any relevant terms and update the next key in state based on this
    if any(term in reply.lower() for term in ["stress", "focus", "overwhelmed, adhd, anxious, anxiety, depression"]):
        state.next = "END" 
    else:
        state.next = "RewriteReply"

    # handling rewrite reply
    if state.next== "END": 
        return state
    
    else:
        state = rewrite_reply(state, llm)
        return state
    


def build_lang_graph():
    """
    Builds and compiles a LangChain workflow (LangGraph) for document retrieval and response generation.
    
    This function creates a graph with two nodes:
    1. "RetrieveRelevantDocs" - Retrieves relevant documents.
    2. "SystemRepliesGenerator" - Generates a response based on the retrieved documents.

    The nodes are connected by edges to form a linear workflow. The workflow starts from "RetrieveRelevantDocs" 
    and proceeds to "SystemRepliesGenerator".
    
    Returns:
        app (StateGraph): A compiled workflow ready for execution.
    """
    
    # Initialize the LangChain StateGraph
    workflow = StateGraph(GraphState)

    # Add nodes to the workflow
    workflow.add_node("RetrieveRelevantDocs", RunnableLambda(retrieve_relevant_docs))
    workflow.add_node("SystemRepliesGenerator", RunnableLambda(generate_response))

    # Define the flow of execution
    workflow.set_entry_point("RetrieveRelevantDocs")
    workflow.add_edge("RetrieveRelevantDocs", "SystemRepliesGenerator")

    # Compile the workflow into an executable app
    app = workflow.compile()

    return app






