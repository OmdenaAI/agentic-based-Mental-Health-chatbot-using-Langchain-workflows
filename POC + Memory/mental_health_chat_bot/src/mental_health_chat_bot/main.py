
from src.mental_health_chat_bot.crew import MentalHealthChatbotCrew
from dotenv import load_dotenv
import os
import datetime


# Load environment variables
load_dotenv()
# print("GOOGLE_API_KEY:", os.getenv("GOOGLE_API_KEY"))  # Debug print

def log_conversation(message: str):
    """Append message to conversation log with timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs/conversation_log.txt", "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def main():
    print("Welcome to the Mental Health Chatbot. I'm here to listen and support you.")
    print("Type 'exit' to end the conversation.\n")
    log_conversation("Chatbot started.")

    conversation_history = []
    while True:
        user_input = input("You: ")
        log_conversation(f"You: {user_input}")
        if user_input.lower() == "exit":
            print("Goodbye. Take care!")
            log_conversation("Chatbot ended.")
            break

        conversation_history.append(f"User: {user_input}")
        inputs = {
            "user_input": user_input,
            "conversation_history": "\n".join(conversation_history[-5:])
        }

        crew = MentalHealthChatbotCrew()
        result = crew.crew().kickoff(inputs=inputs)

        conversation_history.append(f"Bot: {result}")
        print(f"Bot: {result}\n")
        log_conversation(f"Bot: {result}")

if __name__ == "__main__":
    main()