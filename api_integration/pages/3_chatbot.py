import time
import streamlit as st
import sys
import os
from pydub import AudioSegment
from gtts import gTTS
import tempfile
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
import io
import base64
from dotenv import load_dotenv
from src.crewai_knowledge_chatbot.crew import CrewaiKnowledgeChatbot

# Add the current directory to the Python path if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Mental Health Chatbot",
    page_icon="🤖",
    layout="wide",
)

# Check if user data exists in session state (redirect if not)
if "user_data" not in st.session_state or not st.session_state.user_data:
    st.warning("Please complete your profile first!")
    st.switch_page("pages/1_user_form.py")
    st.stop()

# Initialize session state for chatbot
if "input_processed" not in st.session_state:
    st.session_state.input_processed = False
if "user_input" not in st.session_state:
    st.session_state.user_input = False
if "s2s_processed" not in st.session_state:
    st.session_state.s2s_processed = False
if "response_generated" not in st.session_state:
    st.session_state.response_generated = False
if "playback_requested" not in st.session_state:
    st.session_state.playback_requested = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
if "session_id" not in st.session_state:
    st.session_state.session_id = f"user_{hash(st.session_state.user_data.get('name', 'anonymous'))}"

# Add CSS for styling (unchanged, keeping your original styling)
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
}
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

# Create sidebar content
with st.sidebar:
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    # Add information about next steps
    st.title("Mental Health Chatbot")

    with st.expander("**👤 User Profile**"):
                if st.session_state.get('user_data'):
                    user_data = st.session_state.user_data
                    st.markdown(f"**Name:** {st.session_state.user_data['name']}")
                    st.markdown(f"**Age:** {st.session_state.user_data['age']}")
                    st.markdown(f"**Gender:** {st.session_state.user_data['gender']}")
                    st.markdown(f"**Occupation:** {st.session_state.user_data['occupation']}")
                    # Add communication style preference if available
                    #if 'preferred_style' in st.session_state.user_data:
                    #    st.markdown(f"**Communication Style:** {st.session_state.user_data['preferred_style']}")
                    #else:
                    #    st.session_state.user_data['preferred_style'] = "Supportive and empathetic"
                    #    st.markdown(f"**Communication Style:** {st.session_state.user_data['preferred_style']}")

    
    st.markdown("### Chat Controls")
    
    # Download Chat History button
    if st.button("📥 Download Chat History"):
        with open("chat_history.txt", "w") as f:
            for message in st.session_state.history:
                f.write(f"{message}\n")
        st.success("Chat history downloaded successfully!")
    
    # Read Chat History Aloud button
    if st.button("🔊 Read Chat History Aloud"):
        for message in st.session_state.history:
            speak_text(message)
        st.success("Chat history read aloud successfully!")
    
    # Start New Conversation button
    if st.button("🔁 Start New Conversation"):
        for key in ["messages", "history", "user_input", "input_processed", "s2s_processed", "response_generated"]:
            if key in st.session_state:
                if isinstance(st.session_state[key], list):
                    st.session_state[key].clear()
                else:
                    st.session_state[key] = False if "processed" in key or "generated" in key else ""
        st.rerun()
    
    # Return to profile button
    if st.button("✏️ Edit Profile"):
        # Reset necessary session states
        st.session_state.page = "info"
        st.switch_page("pages/1_user_form.py")

    st.markdown("</div>", unsafe_allow_html=True)

# Helper functions
def recognize_speech_from_audio(audio_data_path):
    """Convert audio file to text using Google's speech recognition"""
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
    """Convert text to speech and play it"""
    try:
        tts = gTTS(text)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            st.audio(fp.name, format="audio/mp3")
    except Exception as e:
        st.error(f"Text-to-Speech Error: {e}")

def get_transcript_from_audio(audio_bytes, fmt="webm"):
    """Convert audio bytes to text"""
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

def create_user_context(user_data):
    """Create a structured user context string from user data"""
    return f"""
    User Profile:
    - Name: {user_data.get('name', 'Not provided')}
    - Age: {user_data.get('age', 'Not provided')}
    - Gender: {user_data.get('gender', 'Not provided')}
    - Occupation: {user_data.get('occupation', 'Not provided')}
    - Preferred Communication Style: {user_data.get('preferred_style', 'Supportive and empathetic')}
    """

# Main chatbot UI
st.title(f"Welcome {st.session_state.user_data['name']}! 👋 Let's chat.")

# Show messages
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    avatar = "👤" if role == "user" else "🤖"
    st.markdown(f"{avatar} {role.capitalize()}: {content}")

# Input mode
input_mode = st.radio("Choose input mode:", [
                      "Type", "Speak", "Speech-to-Speech"], horizontal=True)

# User name for greeting
user_name = st.session_state.user_data["name"]

# --- Handle Based on Choice ---
# Input collection
if input_mode == "Type":
    user_input = st.chat_input(
        f"Hi {user_name}, how are you feeling today?")
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
        try:
            # Format conversation history
            chat_history = "\n".join(st.session_state.history)
            
            # Prepare user context including therapy insights if available
            user_context = create_user_context(st.session_state.user_data)
            
            # Add therapy insights if available
            if 'therapy_insights' in st.session_state:
                user_context += f"\nTherapy Insights:\n{st.session_state.therapy_insights}"

            # Prepare inputs for the chatbot crew
            inputs = {
                "user_message": user_input, 
                "history": chat_history,
                "full_context": user_context,
                "preferred_style": st.session_state.user_data.get('preferred_style', 'Supportive and empathetic')
            }

            # Call the chatbot with the prepared inputs
            # Create the chatbot with the session ID
            chatbot = CrewaiKnowledgeChatbot(user_id=st.session_state.session_id)
            result = chatbot.crew().kickoff(inputs=inputs)
            #result = CrewaiKnowledgeChatbot().crew(user_id=st.session_state.session_id).kickoff(inputs=inputs)
            
            # Extract response from result
            if hasattr(result, 'raw'):
                response = result.raw
            else:
                response = str(result)
            
            st.session_state.history.append(f"Assistant: {response}")
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Error generating response: {e}")
            response = "I'm sorry, I encountered an error processing your request. Please try again or rephrase your question."
            st.session_state.history.append(f"Assistant: {response}")
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    st.markdown(f"🤖 Assistant: {response}")
    st.session_state.response_generated = True

    if input_mode in ["Speech-to-Speech", "Speak"]:
        try:
            tts = gTTS(response)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tts_file:
                tts.save(tts_file.name)
                with open(tts_file.name, 'rb') as audio_file:
                    audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')
        except Exception as e:
            st.error(f"Error generating speech: {e}")

# Add a footer
#st.markdown("---")
#st.markdown("Powered by CrewAI and Mem0 | Built with Streamlit")