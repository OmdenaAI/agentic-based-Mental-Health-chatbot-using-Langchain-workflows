
# 🧠 Mental Health Chatbot

An AI-powered voice + text chatbot built with **FastAPI**, **Streamlit**, and **Gemini LLM** to provide helpful mental health guidance. It also logs all conversations to a `chat_log.json` file.

---

## 💡 Features

- 🗣️ Speech-to-text and text-to-speech support by pyaudio
- 💬 Chat interface using Streamlit
- 🧠 Answers powered by Google's Gemini model (`models/gemini-1.5-flash`)
- 📝 Logs all interactions in `chat_log.json`
- 🎥 Comes with a demo video to showcase capabilities

---

## 🚀 How to Run

### 1. Clone the Repo

```bash
git clone <your-repo-url> 
git clone --branch <branch-name> <your-repo-url>
cd Omdena_Mental-Health-Chatbot
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
conda create -n mentalbot python=3.10
conda activate mentalbot
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Make sure `ffmpeg` is installed and available in your PATH.

### 4. Start the Backend (FastAPI)

```bash
uvicorn main:app --reload
```

By default, this runs on `http://127.0.0.1:8000`

### 5. Start the Frontend (Streamlit)

In another terminal:

```bash
streamlit run app.py
```

This launches the chatbot UI in your browser.

---

## 🎤 Example Questions

Try asking the chatbot:

- "I'm feeling overwhelmed, what should I do?"
- "Suggest ways to reduce anxiety."
- "What is mindfulness?"
- "I can't sleep properly. Can you help?"
- "What are symptoms of burnout?"

---

## 📂 Logs

Every conversation is stored in:

```
chat_log.json
```

You can analyze it later for feedback or improvement tracking.



## 🙌 Acknowledgments

Built as part of the Omdena Mental Health Initiative 💚  
Powered by LLMs, FastAPI, and Streamlit.
