import time
from dotenv import load_dotenv
from src.crewai_knowledge_chatbot.crew import CrewaiKnowledgeChatbot
import streamlit as st
# Adjust the import based on your project structure
import sys
import os
from pydub import AudioSegment
from gtts import gTTS
from tempfile import NamedTemporaryFile
from streamlit_mic_recorder import mic_recorder
import speech_recognition as sr
#from streamlit_audio_recorder import audio_recorder ## need to fix this for speech to text
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

# --- User chooses Input Mode ---
input_mode = st.radio(
    "Choose input mode:", 
    ["Type", "Speak"],
    horizontal=True,
)
                
                   
# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
if "input_processed" not in st.session_state:
    st.session_state.input_processed = False

# Create sidebar content
with st.sidebar:
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    st.title("Chatbot details")
    st.markdown("### About")
    st.markdown("This chatbot uses CrewAI and Mem0 to provide context-aware responses using the knowledge from the PDF document. It uses Streamlit for the UI.")

    # Display document info
    #st.markdown("### PDF Information")
    #st.markdown("<div class='document-info'>", unsafe_allow_html=True)
    #st.markdown("📄 **Loaded Document**: CoALA.pdf")
    #st.markdown("**Title**: Cognitive Architectures for Language Agents")
    # st.markdown("</div>", unsafe_allow_html=True)

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    
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
    if gender != "Prefer not to say":
        progress += 25
    if occupation.strip() != "":
        progress += 25      
        
    # Show progress bar
    st.progress(progress, text=f"Profile Completion: {progress}%")

    # Button to submit info
    all_fields_completed = (progress == 100)

    if all_fields_completed:
        if st.button("✅ Submit and Start Chat"):
            st.session_state.user_data = {
                "name": name,
                "age": age,
                "gender": gender,
                "occupation": occupation,
            }
            st.session_state.page = "chat"
    else:
        st.info("ℹ️ Please complete all fields to start the chat.")


# Check if page state is initialized
if "page" not in st.session_state:
    st.session_state.page = "info"

# Force back to info if user_data is missing
if st.session_state.page == "chat" and "user_data" not in st.session_state:
    st.session_state.page = "info"
    st.rerun()

# Main flow
if st.session_state.page == "info":
    collect_user_info()
elif st.session_state.page == "chat":
    st.title(f"Welcome {st.session_state.user_data['name']}! 👋 Let's chat.")

    # Display chat messages
    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "🤖"
        avatar_class = "user-avatar" if message["role"] == "user" else "assistant-avatar"
        message_class = "user" if message["role"] == "user" else "assistant"

        st.markdown(f"""
        <div class="chat-message {message_class}">
            <div class="avatar {avatar_class}">{avatar}</div>
            <div class="content">
                <p class="chat-message-text">{message["content"]}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Chat input
    user_name = st.session_state.user_data["name"]
    user_input = st.chat_input(f"Hi {user_name}, how are you feeling today?")

    #user_message = None  # Initialize
    audio_bytes = None

    # --- Handle Based on Choice ---
    if input_mode == "Type":
        user_input
        
    elif input_mode == "Speak" :
        # st.write("🎤 Click below and speak your message:")
        if st.session_state.input_processed:
            if st.button("🎤 Speak Again"):
                st.session_state.input_processed = False
                st.rerun()
        if not st.session_state.input_processed :
            # audio_bytes = audio_recorder(pause_threshold=1.0)
            audio_data = mic_recorder(start_prompt="Start recording", stop_prompt="Stop recording", use_container_width=True)
            

            
            if audio_data :
                audio_bytes = audio_data['bytes']
                # with open("temp_audio.wav", "wb") as f:
                #     f.write(audio_bytes)
                # user_message = recognize_speech_from_audio("temp_audio.wav")
                try:
                    audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="webm")  # format might need to be changed
                    audio_segment.export("temp_audio.wav", format="wav")
                    user_input = recognize_speech_from_audio("temp_audio.wav")
                    if user_input:
                        st.success(f"Recognized: {user_input}")
                        st.session_state.input_processed = True
                        
                    
                    # Add "Listen Again" button
                    if st.button("🔊 Listen to my message again"):
                        # Playback the recorded audio
                        st.audio(audio_bytes, format="audio/wav")
                        
                except Exception as e:
                    st.error(f"Audio Conversion Error: {e}")
                    
                    
        # Process user input
    if user_input:
        # Add user message to chat
        st.session_state.messages.append(
            {"role": "user", "content": user_input})
        st.session_state.history.append(f"User: {user_input}")

        # Display user message (immediate feedback)
        st.markdown(f"""
        <div class="chat-message user">
            <div class="avatar user-avatar">👤</div>
            <div class="content">
                <p class="chat-message-text">{user_input}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Create "typing" indicator
        with st.spinner("Thinking..."):
            # Format history for the CrewAI chatbot
            chat_history = "\n".join(st.session_state.history)

            # Process with CrewAI
            inputs = {
                "user_message": user_input,
                "history": chat_history
            }

            # Get response from CrewAI
            # Note: This might take some time depending on the complexity
            response = CrewaiKnowledgeChatbot().crew().kickoff(inputs=inputs)

            # Update history
            st.session_state.history.append(f"Assistant: {response}")

        # Add assistant response to messages
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
                
        # Display assistant message (using markdown for better formatting)
        st.markdown(f"""
        <div class="chat-message assistant">
            <div class="avatar assistant-avatar">🤖</div>
            <div class="content">
                <p class="chat-message-text">{response}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Force a rerun to update the UI
        # user_input = None
        # audio_bytes = None
        st.rerun()

# if st.button("🎙️ Click to Start New Recording"):
#     st.session_state.input_processed = False       
        
# Add a button to download the chat history
if st.button("Download Chat History"):
    with open("chat_history.txt", "w") as f:
        for message in st.session_state.history:
            f.write(f"{message}\n")
    st.success("Chat history downloaded successfully!")

def speak_text(text):
    tts = gTTS(text)
    with NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3")
        
# Add a button to read the chat history aloud
if st.button("Read Chat History Aloud"):
    for message in st.session_state.history:
        speak_text(message)
    st.success("Chat history read aloud successfully!")

        
# Add a footer
st.markdown("---")
st.markdown("Powered by CrewAI and Mem0 | Built with Streamlit")
