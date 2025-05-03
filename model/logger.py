import json
from datetime import datetime

def log_conversation(user_query, bot_response, log_file="chat_log.json"):
    try:
        with open(log_file, "r") as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    logs.append({
        "timestamp": datetime.now().isoformat(),
        "user": user_query,
        "assistant": bot_response
    })

    with open(log_file, "w") as f:
        json.dump(logs, f, indent=2)
