from src.crewai_knowledge_chatbot.crew import CrewaiKnowledgeChatbot

def get_response(user_message, history):
    chat_history = "\n".join(history)
    inputs = {
        "user_message": user_message,
        "history": chat_history,
    }
    response = CrewaiKnowledgeChatbot().crew().kickoff(inputs=inputs)
    return str(response)