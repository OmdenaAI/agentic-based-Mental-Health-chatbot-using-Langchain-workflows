#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from crewai_knowledge_chatbot.crew import CrewaiKnowledgeChatbot
from mem0 import MemoryClient

client = MemoryClient()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="chromadb")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="mem0")
warnings.filterwarnings("ignore", message=".*'model_fields' attribute.*")
warnings.filterwarnings("ignore", message=".*output_format='v1.0' is deprecated.*")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    history = []
    """
    Run the crew.
    """
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye! It was nice talking to you.")
            break

        chat_history = "\\n".join(history)

        inputs = {
            "user_message": f"{user_input}",
            "history": f"{chat_history}",
        }

        response = CrewaiKnowledgeChatbot().crew().kickoff(inputs=inputs)
        history.append(f"User: {user_input}")
        history.append(f"Assistant: {response}")
        client.add(user_input, user_id="User")

        print(f"Assistant: {response}")
    #try:
    #    CrewaiKnowledgeChatbot().crew().kickoff(inputs=inputs)
    #except Exception as e:
    #    raise Exception(f"An error occurred while running the crew: {e}")