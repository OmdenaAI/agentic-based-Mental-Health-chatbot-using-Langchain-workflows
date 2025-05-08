import time
from dotenv import load_dotenv
from src.crewai_knowledge_chatbot.crew import CrewaiKnowledgeChatbot
import streamlit as st
# Adjust the import based on your project structure
import sys
import os
from pydub import AudioSegment
from gtts import gTTS
import tempfile
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import io
import base64


# Add the current directory to the Python path if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try alternative import paths - uncomment the one that works
# Import approach 1: If your main file is in src/crewai_knowledge_chatbot/crew.py

# Import approach 2: If your main file is at the root level
# from crew import CrewaiKnowledgeChatbot

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Mental Health Chatbot",
    page_icon="🤖",
    layout="wide",
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
if "input_processed" not in st.session_state:
    st.session_state.input_processed = False
if "user_data" not in st.session_state:
    st.session_state.user_data = False
if "user_input" not in st.session_state:
    st.session_state.user_input = False
if "s2s_processed" not in st.session_state:
    st.session_state.s2s_processed = False
if "response_generated" not in st.session_state:
    st.session_state.response_generated = False
if "playback_requested" not in st.session_state:
    st.session_state.playback_requested = False

# Add CSS for styling
st.markdown("""
<style>
.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: row;
    align-items: flex-start;
}
.chat-message.user {
    background-color: #f0f2f6;
    color: #000000; /* BLACK text for users */
}
.chat-message.assistant {
    background-color: #e3f2fd;
    color: #000000; /* BLACK text for assistants */
}
.chat-message-text {
    font-size: 16px; /* Make text size comfortable */
    line-height: 1.5; /* More breathing space between lines */
.chat-message .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
}
.chat-message .user-avatar {
    background-color: #6c757d;
    color: white;
}
.chat-message .assistant-avatar {
    background-color: #2196f3;
    color: white;
}
.chat-message .content {
    flex-grow: 1;
    padding-left: 0.5rem;
}
.chat-message-text {
    margin-bottom: 0;
}
.sidebar-content {
    padding: 1rem;
}
.document-info {
    margin-top: 1rem;
    padding: 1rem;
    background-color: #f8f9fa;
    border-radius: 0.5rem;
}
.stButton button {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)


def recognize_speech_from_audio(audio_data_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_data_path) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        return text
    except Exception as e:
        st.error(f"Speech Recognition Error: {e}")
        return ""


def speak_text(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3")


# Create sidebar content
with st.sidebar:
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    st.title("Chatbot details")
    st.markdown("### About")
    st.markdown("This chatbot uses CrewAI and Mem0 to provide context-aware responses using the knowledge from the PDF document. It uses Streamlit for the UI.")

    # Display document info
    # st.markdown("### PDF Information")
    # st.markdown("<div class='document-info'>", unsafe_allow_html=True)
    # st.markdown("📄 **Loaded Document**: CoALA.pdf")
    # st.markdown("**Title**: Cognitive Architectures for Language Agents")
    st.markdown("</div>", unsafe_allow_html=True)

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# Check if page state is initialized
if "page" not in st.session_state:
    st.session_state.page = "info"

# Function to display chat messages


def collect_user_info():
    st.title("🤖 Mental Health Chatbot - User Information")

    # Collect basic info
    name = st.text_input("What is your name?")
    age = st.number_input("What is your age?",
                          min_value=1, max_value=120, step=1)
    gender = st.selectbox("What is your gender?", [
                          "Prefer not to say", "Male", "Female", "Other"])
    occupation = st.text_input("What is your occupation?")

    # Progress calculation
    progress = 0
    if name.strip() != "":
        progress += 25
    if age is not None and age > 0:
        progress += 25
    if gender != "":
        progress += 25
    if occupation.strip() != "":
        progress += 25

    # Show progress bar
    st.progress(progress, text=f"Profile Completion: {progress}%")

    # Button to submit info
    if progress == 100 and st.button("✅ Submit and Start Chat"):
        st.session_state.user_data = {
            "name": name, "age": age, "gender": gender, "occupation": occupation}
        st.session_state.page = "chat"


if st.session_state.page == "info":
    collect_user_info()
    st.stop()

# Helper function to convert speech to text


def get_transcript_from_audio(audio_bytes, fmt="webm"):
    try:
        audio_segment = AudioSegment.from_file(
            io.BytesIO(audio_bytes), format=fmt)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
            audio_segment.export(tmp_wav.name, format="wav")
            recognizer = sr.Recognizer()
            with sr.AudioFile(tmp_wav.name) as source:
                audio = recognizer.record(source)
                return recognizer.recognize_google(audio)
    except Exception as e:
        st.error(f"Speech Recognition Error: {e}")
        return ""


# Chat page
st.title(f"Welcome {st.session_state.user_data['name']}! 👋 Let's chat.")

# Show messages
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    avatar = "👤" if role == "user" else "🤖"
    st.markdown(f"{avatar} {role.capitalize()}: {content}")

# Input mode
input_mode = st.radio("Choose input mode:", [
                      "Type", "Speak", "Speech-to-Speech"], horizontal=True)

# Chat input
user_name = st.session_state.user_data["name"]


# --- Handle Based on Choice ---
# Input collection
if input_mode == "Type":
    user_input = st.chat_input(
        f"Hi {st.session_state.user_data['name']}, how are you feeling today?")
    if user_input:
        st.session_state.user_input = user_input
        st.session_state.input_processed = True
        st.session_state.response_generated = False

elif input_mode == "Speak":
    if st.session_state.input_processed:
        if st.button("🎤 Speak Again"):
            st.session_state.input_processed = False
            st.session_state.response_generated = False
            st.session_state.playback_requested = False
            st.rerun()
    else:
        audio_data = mic_recorder(
            "Start recording", "Stop recording", use_container_width=True)
        if audio_data:
            audio_bytes = audio_data['bytes']
            if st.button("🔊 Listen to your voice again"):
                st.audio(audio_bytes, format="audio/wav")
                st.session_state.playback_requested = True
            transcript = get_transcript_from_audio(audio_bytes)
            if transcript:
                st.session_state.user_input = transcript
                st.session_state.input_processed = True
                st.session_state.response_generated = False
                st.success(f"Recognized: {transcript}")

elif input_mode == "Speech-to-Speech" and not st.session_state.s2s_processed:
    audio = mic_recorder(start_prompt="🎤 Start Talking",
                         stop_prompt="⏹️ Stop", key="mic")
    if audio:
        if st.button("🔊 Listen to your voice again"):
            st.audio(audio['bytes'], format='audio/wav')
            st.session_state.playback_requested = True
        transcript = get_transcript_from_audio(audio['bytes'])
        if transcript:
            st.session_state.user_input = transcript
            st.session_state.input_processed = True
            st.session_state.response_generated = False
            st.session_state.s2s_processed = True
            st.success(f"You said: {transcript}")

# Response generation
if st.session_state.input_processed and st.session_state.user_input and not st.session_state.response_generated:
    if (input_mode in ["Speak", "Speech-to-Speech"]) and st.session_state.get("playback_requested"):
        time.sleep(2)
    user_input = st.session_state.user_input
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.history.append(f"User: {user_input}")
    st.markdown(f"👤 You: {user_input}")
    with st.spinner("Thinking..."):
        chat_history = "\n".join(st.session_state.history)
        inputs = {"user_message": user_input, "history": chat_history}
        response = str(CrewaiKnowledgeChatbot().crew().kickoff(inputs=inputs))
        st.session_state.history.append(f"Assistant: {response}")
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
    st.markdown(f"🤖 Assistant: {response}")
    st.session_state.response_generated = True

    if input_mode in ["Speech-to-Speech", "Speak"]:
        tts = gTTS(response)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tts_file:
            tts.save(tts_file.name)
            with open(tts_file.name, 'rb') as audio_file:
                audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')

# Add a button to download the chat history
if st.button("Download Chat History"):
    with open("chat_history.txt", "w") as f:
        for message in st.session_state.history:
            f.write(f"{message}\n")
    st.success("Chat history downloaded successfully!")


# Add a button to read the chat history aloud
if st.button("Read Chat History Aloud"):
    for message in st.session_state.history:
        speak_text(message)
    st.success("Chat history read aloud successfully!")

if st.button("🔁 Start New Conversation"):
    for key in ["messages", "history", "user_input", "input_processed", "s2s_processed", "response_generated"]:
        if isinstance(st.session_state[key], list):
            st.session_state[key].clear()
        else:
            st.session_state[key] = False if "processed" in key or "generated" in key else ""
    st.rerun()

# Add a footer
st.markdown("---")
st.markdown("Powered by CrewAI and Mem0 | Built with Streamlit")
