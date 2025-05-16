from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from datetime import datetime
import os
import json
import csv
import requests
from mentalhealth_chatbot.crew import MentalHealthChatbotCrew
from sentence_transformers import SentenceTransformer
import faiss
import pyttsx3
from tools.custom_rag_tool import CustomRAGTool
from collections import defaultdict
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://ortal.ngrok.io"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

crew = MentalHealthChatbotCrew()
rag_tool = CustomRAGTool()

os.makedirs("logs", exist_ok=True)
os.makedirs("embeddings", exist_ok=True)

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.IndexFlatL2(384)

user_sessions = {}  # user_id → {"consent": bool, "mode": str}
conversation_history = []

# WhatsApp
VERIFY_TOKEN = "mentalhealth123"
PAGE_ACCESS_TOKEN = os.getenv("WHATSAPP_PAGE_TOKEN", "")

# ------------------ Schemas ------------------

class InitSessionInput(BaseModel):
    user_id: str
    consent: bool
    mode: str

class ChatInput(BaseModel):
    user_id: str
    user_input: str

class SurveyInput(BaseModel):
    user_id: str
    mood_score: int
    stress_score: int
    notes: str = ""

class UserProfileInput(BaseModel):
    user_id: str
    age: str
    gender: str
    employment_status: str
    financial_worries: str
    mental_issues: list[str]
    consent: bool

# ------------------ Helpers ------------------

def log_message(user_id, user_input, bot_response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs/conversation_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {user_id} - You: {user_input}\n")
        f.write(f"[{timestamp}] {user_id} - Bot: {bot_response}\n")

def log_insight(user_id, emotion, suggestions):
    today = datetime.now().strftime("%Y-%m-%d")
    filepath = "logs/user_insights.csv"
    file_exists = os.path.isfile(filepath)
    with open(filepath, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["user_id", "date", "emotion", "suggestions"])
        writer.writerow([user_id, today, emotion, suggestions])

def save_embedding(user_id, text):
    embedding = embedding_model.encode([text])
    index.add(embedding)

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    zira_voice = next((v for v in voices if "Zira" in v.name), None)

    if zira_voice:
        engine.setProperty('voice', zira_voice.id)
        print(f"✅ Using voice: {zira_voice.name}")
    else:
        print("⚠️ Zira voice not found. Using default.")

    engine.say(text)
    engine.runAndWait()
    engine.stop()

def send_whatsapp_reply(to: str, message: str):
    url = "https://graph.facebook.com/v17.0/me/messages"
    headers = {
        "Authorization": f"Bearer {PAGE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }
    requests.post(url, headers=headers, json=payload)

# ------------------ Routes ------------------

@app.post("/init_session")
def init_session(data: InitSessionInput):
    if data.mode not in ["text", "voice"]:
        raise HTTPException(status_code=400, detail="Mode must be 'text' or 'voice'.")
    if not data.consent:
        raise HTTPException(status_code=403, detail="Consent required to proceed.")
    user_sessions[data.user_id] = {"consent": True, "mode": data.mode}
    return {"status": "Session initialized.", "mode": data.mode}

@app.post("/chat")
def chat(input: ChatInput):
    session = user_sessions.get(input.user_id)
    if not session:
        raise HTTPException(status_code=403, detail="Session not initialized.")

    conversation_history.append(f"User: {input.user_input}")
    inputs = {
        "user_input": input.user_input,
        "conversation_history": "\n".join(conversation_history[-5:])
    }

    try:
        crew_instance = crew.crew()
        result = crew_instance.kickoff(inputs=inputs)
        safety_output = result.get("safety_result", "{}") if isinstance(result, dict) else "{}"
    except Exception as e:
        result = f"Error: {str(e)}"
        safety_output = "{}"

    final_response = str(result.get("final_response", result)) if isinstance(result, dict) else str(result)
    conversation_history.append(f"Bot: {final_response}")
    log_message(input.user_id, input.user_input, final_response)
    save_embedding(input.user_id, input.user_input)
    log_insight(input.user_id, emotion="unknown", suggestions="parsed from result")

    try:
        safety_data = json.loads(safety_output)
        if safety_data.get("distress") is True:
            flagged = safety_data.get("trigger", "unknown")
            phone = None
            try:
                with open("logs/user_profiles.csv", "r", encoding="utf-8") as f:
                    for row in reversed(list(csv.DictReader(f))):
                        if row["user_id"] == input.user_id:
                            phone = row.get("guardian_phone", "") or row.get("therapist_phone", "")
                            break
            except:
                pass
            if phone:
                alert_msg = f"🚨 Mental health alert: distress detected.\nTrigger: \"{flagged}\""
                send_whatsapp_reply(phone, alert_msg)
    except Exception as e:
        print("Error parsing safety output:", e)

    if session["mode"] == "voice":
        speak(final_response)

    return {
        "response": final_response,
        "mode": session["mode"]
    }

@app.post("/survey")
def submit_survey(data: SurveyInput):
    today = datetime.now().strftime("%Y-%m-%d")
    filepath = "logs/user_insights.csv"
    file_exists = os.path.isfile(filepath)
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["user_id", "date", "mood_score", "stress_score", "notes"])
        writer.writerow([data.user_id, today, data.mood_score, data.stress_score, data.notes])
    return {"status": "Survey saved."}

@app.post("/user_profile")
def submit_profile(data: UserProfileInput):
    today = datetime.now().strftime("%Y-%m-%d")
    filepath = "logs/user_profiles.csv"
    file_exists = os.path.isfile(filepath)
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["user_id", "date", "age", "gender", "employment_status", "financial_worries", "mental_issues", "consent"])
        writer.writerow([
            data.user_id,
            today,
            data.age,
            data.gender,
            data.employment_status,
            data.financial_worries,
            "; ".join(data.mental_issues),
            data.consent
        ])
    return {"status": "Profile saved."}

@app.post("/profile_feedback")
def profile_feedback(data: UserProfileInput):
    try:
        prompt = f"""
        Age: {data.age}
        Gender: {data.gender}
        Employment Status: {data.employment_status}
        Financial Worries: {data.financial_worries}
        Mental Issues: {", ".join(data.mental_issues)}
        Consent Given: {data.consent}
        Provide a personalized mental health well-being message.
        """

        print("📌 Prompt sent to CrewAI:\n", prompt)

        crew_instance = crew.crew()
        result = crew_instance.kickoff(inputs={"user_input": prompt})

        final = result.get("final_response") if isinstance(result, dict) else result
        return {"feedback": final}

    except Exception as e:
        import traceback
        print("❌ Error generating feedback:")
        traceback.print_exc()
        return {"feedback": "Error generating feedback. Please try again later."}

@app.get("/dashboard-data")
def dashboard_data(user_id: str = None):
    insights_path = "logs/user_insights.csv"
    results = {
        "mood_by_date": defaultdict(list),
        "stress_by_date": defaultdict(list),
        "emotions": defaultdict(int)
    }
    if not os.path.exists(insights_path):
        return results
    with open(insights_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if user_id and row["user_id"] != user_id:
                continue
            date = row["date"]
            mood = int(row.get("mood_score", 0))
            stress = int(row.get("stress_score", 0))
            emotion = row.get("emotion", "unknown")
            results["mood_by_date"][date].append(mood)
            results["stress_by_date"][date].append(stress)
            results["emotions"][emotion] += 1
    return {
        "mood_by_date": {k: sum(v)/len(v) for k, v in results["mood_by_date"].items()},
        "stress_by_date": {k: sum(v)/len(v) for k, v in results["stress_by_date"].items()},
        "emotions": results["emotions"]
    }

@app.get("/webhook")
async def verify_token(request: Request):
    params = dict(request.query_params)
    if params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(params["hub.challenge"])
    return {"error": "Invalid verification token"}

frontend_path = Path(__file__).resolve().parent.parent.parent / "mentalhealth-frontend" / "build"
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")

@app.get("/")
async def serve_react():
    return FileResponse(frontend_path / "index.html")
