"""Models for the application."""

# Importing necessary libraries
from typing import Annotated, Optional
from enum import Enum
from pydantic import BaseModel
from langgraph.graph.message import add_messages



class Gender(str, Enum):
    """
    Enum representing gender options.

    Attributes:
        male (str): Represents a male gender.
        female (str): Represents a female gender.
        other (str): Represents a non-binary or unspecified gender.
    """

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class Emotion(str, Enum):
    """
    Enum representing Emotion options.

    Attributes:
        Anxiety (str): Represents anxiety as an emotion.
        Stress (str): Represents stress as an emotion.
        Attention-Deficit/Hyperactivity Disorder (ADHD) (str): Represents ADHD as an emotion.
        Depression: Represents depression as an emotion.
    """

    ANXIETY = "anxiety"
    STRESS = "stress"
    ADHD = "ADHD"
    DEPRESSION = "Depression"


class Language(str, Enum):
    """
    Enum representing language options.

    Attributes:
        English (str): Represents the English Language.
    """

    ENGLISH = "english"



class SentenceTransformers(str, Enum):

    """
    Enum representing various pre-trained SentenceTransformer model names.

    These models are commonly used for embedding sentences into vector space
    for tasks like semantic similarity, clustering, or retrieval. The string
    values correspond to model names available in the Hugging Face model hub.
    """

    ALL_MPNET_BASE_V2 = "all-mpnet-base-v2"
    MULTI_QA_MPNET_BASE_DOT_V1 = "multi-qa-mpnet-base-dot-v1"
    ALL_DISTILROBERTA_V1 = "all-distilroberta-v1"
    ALL_MINILM_L12_V2 = "all-MiniLM-L12-v2"
    MULTI_QA_DISTILBERT_COS_V1 = "multi-qa-distilbert-cos-v1"
    ALL_MINILM_L6_V2 = "all-MiniLM-L6-v2"
    MULTI_QA_MINILM_L6_COS_V1 = "multi-qa-MiniLM-L6-cos-v1"
    PARAPHRASE_MULTILINGUAL_MPNET_BASE_V2 = "paraphrase-multilingual-mpnet-base-v2"
    PARAPHRASE_ALBERT_SMALL_V2 = "paraphrase-albert-small-v2"
    PARAPHRASE_MULTILINGUAL_MINILM_L12_V2 = "paraphrase-multilingual-MiniLM-L12-v2"
    PARAPHRASE_MINILM_L3_V2 = "paraphrase-MiniLM-L3-v2"
    DISTILUSE_BASE_MULTILINGUAL_CASED_V1 = "distiluse-base-multilingual-cased-v1"
    DISTILUSE_BASE_MULTILINGUAL_CASED_V2 = "distiluse-base-multilingual-cased-v2" 



class GraphState(BaseModel):
    """
    Represents the state of a conversation in the chatbot.

    Attributes:
        messages (list): A list of messages as entered by the User that will be processed by the `add_messages` function.
        age (int): The age of the User interacting with the chatbot.
        gender (str): The gender of the User.
        language (Optional[str]): The language of the User. This field is optional and may be `None`.
        emotion (str): The current emotional state of the User.
        query (str): The User's query or request.
        docs (list): A list of documents relevant to the query.
        next (str): The next action or step in the interaction, e.g., "ask another question", "end conversation".

    Note:
        The `messages` field is automatically processed by the `add_messages` function to ensure that
        the list is initialized or modified as needed before further processing.
    """

    messages: Annotated[list, add_messages] = []
    age: int = 50
    emotion: Emotion = Emotion.STRESS
    gender: Gender = Gender.FEMALE
    language: str
    query: str 
    docs: list = []
    next: str


class TTSInput(BaseModel):
    text: str





