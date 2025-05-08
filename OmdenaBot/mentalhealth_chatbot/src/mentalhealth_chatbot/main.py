from mentalhealth_chatbot.crew import MentalHealthChatbotCrew
import datetime
import os

def log_conversation(message: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs("logs", exist_ok=True)
    with open("logs/conversation_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def get_bot_response(user_input, conversation_history, context=None):
    conversation_history.append(f"User: {user_input}")

    # Add context if available
    context_info = f"User completed assessments: {', '.join(context)}.\n" if context else ""

    inputs = {
        "user_input": user_input,
        "conversation_history": context_info + "\n".join(conversation_history[-5:])
    }

    try:
        crew = MentalHealthChatbotCrew()
        result = crew.kickoff(inputs=inputs)  # ✅ FIXED
    except Exception as e:
        result = "Oops! Something went wrong. Please try again later."
        print(f"[ERROR] {e}")

    conversation_history.append(f"Bot: {result}")
    log_conversation(f"You: {user_input}")
    log_conversation(f"Bot: {result}")
    return result, conversation_history

def run():
    response, history = get_bot_response("Hello, are you okay?", [])
    print("🧠 Bot:", response)

if __name__ == "__main__":
    run()
