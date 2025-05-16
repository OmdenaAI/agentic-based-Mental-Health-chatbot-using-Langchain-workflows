# 🧠 OmdenaBot: Agentic Mental Health Chatbot

🚀 **About the Project**
This repository hosts the OmdenaBot, an AI-powered mental health chatbot developed using the CrewAI framework, FastAPI, and Meta Cloud Platform (MCP). Designed to support both users and therapists, this system aims to offer real-time feedback, emotional analysis, and potential future predictions.

🔗 **Omdena Challenge Page**
📌 Challenge Title: [Building Agentic-based Mental Health Chatbot using Langchain Workflows](https://www.omdena.com/chapter-challenges/building-agentic-based-mental-health-chatbot-using-langchain-workflows)

🎯 **Objectives**
- Provide personalized feedback and mental health tips.

- Use LLM agents for emotionally adaptive responses with grounded knowledge folder containing necessery docs from data collection.

- Build RAG-based retrieval, multi-agent flow, and real-time insights.

- Enable dashboard tracking - **under construction**
  
- Enable crisis alerts, and integration with third-party (authorized by user) support, for the benefite of both user and his therapist, via Meta's MCP connection to Whatsup API. - **under construction**
  
- Enable profile feedback scoring (GAD) - **under construction**
  
- Enable excercises by extracting bot's response into an interactive activity. - For example: If it's a kid, then it might be a link to a game or meditation excercise according to bot's response (trigger words) - **under construction**
  
- Enable dashboard monthly report download or sent via whatsup for user/therapist, maybe even for research (The user cosents his details and conversations are being recorded) - **under construction**
  
- Further implementations can be : User feedback (like/didn't like the bot's response) , logs folder saves csv's for later analysis and predictions on users profiles according to their inputs. Also making the app a multi user app for all family or for a therapist list of patients. **under construction**


🔍 **Market Research**

📊 Presentation: [Market Overview & Use Cases](https://docs.google.com/presentation/d/1IzzwJpUkDswqyJpZbwAx7E7cB9qPgZnbobUgx853Q6c/edit?usp=sharing)

🧠 **POC & Demo's including basic POC code flow :** [Slides](https://docs.google.com/presentation/d/1N9d8wSF8kq7dHhkAIzcT95hkh9LfAEhcETW2mRj32Ag/edit?usp=sharing)

Big **Thank you for Team1's AI engineers** for creating this awesome unified **CrewAI framework based POC** and Demo's : 

- [Anandhu P Raj](https://github.com/ScopeUnderscore)
- [Indumathy Devanathasamy](https://github.com/Indumathyprabu)
- And special **Thank you to my co lead and AI collaborator** [Sundaravadivu Marimuthu](https://github.com/vadivu123)
- **Thank you for all of [Team1's collaborators](https://docs.google.com/spreadsheets/d/1fvcuyDjEVlxoB0DEkqtMN7NQzrMVxCFs/edit?usp=sharing&ouid=108623279518071003366&rtpof=true&sd=true)**

💼 **Business Question**
# How can AI be used to deliver early-stage mental health interventions that are scalable, emotionally adaptive, and ethically responsible for users in distress — while enabling insights for professionals without breaching trust or privacy?


# 🧠 Mental Health Chatbot (OmdenaBot)

This is a full-stack AI-powered mental health assistant built during an Omdena Challenge. It includes:
- A **FastAPI backend** with agentic logic via CrewAI.
- A **React frontend** for engaging user interaction.
- Integration with **ngrok** for public access via a stable URL.

---

## 🚀 Live Demo

> 🌐 **App is deployed at:**  
> [https://ortal.ngrok.io](https://ortal.ngrok.io)

---

## 📁 Project Structure

mentalhealth_chatbot/
│
├── mentalhealth-frontend/ # React frontend
├── src/ # Backend logic (CrewAI agents, tools, tasks)
├── logs/ # (Create this folder manually to store logs)
├── .env # Environment variables (create based on .env.template)
├── requirements.txt # Python dependencies
├── pyproject.toml # Poetry or pip build configuration
├── uv.lock # Rename the file if necessary
└── README.md # This file


---

## 🛠️ Prerequisites

Make sure you have the following installed:

- Python 3.10 or higher
- Node.js (for frontend)
- `pip` or `poetry`
- `ngrok` (for tunneling)
- Git

---

## ⚙️ Backend Setup

1. **Clone the repository:**

```
git clone https://github.com/ortall0201/OmdenaBot.git
cd OmdenaBot/OmdenaBotUpdated/mentalhealth_chatbot
```

2. **Create a virtual environment and activate it:**
   ```
   python -m venv venv
   ```
- venv\Scripts\activate        # On Windows (This project was built in windows operation system)
- source venv/bin/activate   # On macOS/Linux

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
4.  **Set up .env:**
   
   * Rename the provided .env.template to .env
   * Add your actual API keys where indicated

5. **Create required folders:**
   ```
   mkdir logs
   ```

6. **Run the backend:**
   ```
   set PYTHONPATH=src && uvicorn mentalhealth_chatbot.app:app --reload
   ```
_______________________________________________________________________________________________________

  💻 # **Frontend Setup :**
  
1. **Navigate to the frontend folder:**
   ```
   cd mentalhealth-frontend
   ```
2. **Install frontend dependencies:**
   ```
   npm install
   ```
3. **Start the frontend server:**
   ```
   npm start
   ```
4. If port is busy, allow the prompt to select a new one.

_______________________________________________________________________________________________________

   🌐 # **Public Deployment via ngrok :**

   If you want others to access your app publicly:
   ```
   ngrok http 3000
   ```
Use the generated https://xyz.ngrok.io as your public URL.

⚠️ **This project's version is already deployed via:**
   ```
   https://ortal.ngrok.io
   ```
  FastAPI can be seen in this URL:
  ```
  https://ortal.ngrok.io/docs#/
  ```
Note: The ngrok URL's are working only when backend is connected and running on Visual Studio.
_______________________________________________________________________________________________________

   🧠 # **CrewAI Agent System :**

   This app runs using CrewAI and LangChain, with multiple agents such as:
   * Knowledge Retriever
   * Knowledge Summarizer
   * Workflow Orchestrator

   All logic is defined inside src/agents.yaml, src/tasks.yaml, and crew.py.

 _______________________________________________________________________________________________________

  📝 # **Notes :**

    * The .env file must be configured correctly for the app to work.

    * Make sure uv.lock is renamed properly if needed.

    * Pushes to GitHub require that untracked files are added and committed properly.

_______________________________________________________________________________________________________

  📬 # **Feedback :**

    Feel free to open issues or submit pull requests if you'd like to collaborate or report bugs.

    © 2025 Team1 & Omdena Collaborators
    Built with ❤️ for social good.

_______________________________________________________________________________________________________

   📬 # **Contact :**

   Co Lead of Team1 / Product Owner / Creator of this Repo : Ortalgr@gmail.com
   
    - Team1 details:
![image](https://github.com/user-attachments/assets/e95dccf7-cc2f-4716-8814-1fb9fbfaaa9f)

    

    










   


