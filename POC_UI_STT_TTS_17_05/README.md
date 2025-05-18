# 🧠 Omdena MindfulChat – Mental Health Chatbot (Team 1)

This is a voice-enabled, agentic AI-based mental health chatbot developed using **CrewAI**, **FastAPI**, and **React**. It provides users with personalized self-care suggestions, multi-step mental health assessments, and voice/text interactions — powered by Retrieval-Augmented Generation (RAG) and LangChain memory.

## 🚀 Features

- ✨ **CrewAI Multi-Agent Architecture**: EmotionDetector, SuggestionAgent, SafetyAgent, RAGRetriever, RAGReader  
- 🔍 **RAG Search**: Uses HuggingFace embeddings and FAISS vector database for tip retrieval  
- 🧠 **LLM Integration**: Gemini 2.0 Flash via API key (no Google Cloud dependency)  
- 🗣️ **Voice Interaction**: Whisper for STT and pyttsx3 for TTS  
- 🧪 **Assessments**: Multi-step surveys (Stress, Anxiety, Depression, FOMO) with conditional logic  
- 💾 **Memory**: LangChain `ConversationBufferMemory` + CSV-based session logging

## 🧰 Tech Stack

- **Frontend**: React + TailwindCSS  
- **Backend**: FastAPI (Python)  
- **LLM**: Gemini 2.0 Flash  
- **Embeddings**: HuggingFace (MiniLM-L6-v2)  
- **Vector DB**: FAISS  
- **Voice Tools**: Whisper (STT), pyttsx3 (TTS)  
- **Agents**: CrewAI with YAML config  
- **Memory**: LangChain + CSV logs

## ⚙️ Setup Instructions

```bash
# 1️⃣ Clone the Repository
git clone https://github.com/OmdenaAI/agentic-based-Mental-Health-chatbot-using-Langchain-workflows.git
cd agentic-based-Mental-Health-chatbot-using-Langchain-workflows
git checkout team1
cd POC_UI_STT_TTS_10_5

# 2️⃣ Backend Setup (FastAPI)
python -m venv venv
venv\Scripts\activate   # for windows
cd mentalhealth_chatbot
pip install .

# Create a .env file inside mentalhealth_chatbot with:
# GEMINI_API_KEY=your_gemini_api_key_here

uvicorn fastapi_app.main:app --reload

# 3️⃣ Frontend Setup (React)
# Open a new terminal and run:
cd POC_UI_STT_TTS_10_5/frontend
npm install
npm start

# 4️⃣ Open in Browser
# Visit:
http://localhost:3000
