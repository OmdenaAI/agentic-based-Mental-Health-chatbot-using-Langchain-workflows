from mentalhealth_chatbot.crew import MentalHealthChatbotCrew
import datetime

def log_conversation(message: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs/conversation_log.txt", "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def get_bot_response(user_input, conversation_history):
    conversation_history.append(f"User: {user_input}")
    inputs = {
        "user_input": user_input,
        "conversation_history": "\n".join(conversation_history[-5:])
    }
    crew = MentalHealthChatbotCrew()
    result = crew.crew().kickoff(inputs=inputs)
    conversation_history.append(f"Bot: {result}")
    log_conversation(f"You: {user_input}")
    log_conversation(f"Bot: {result}")
    return result, conversation_history
