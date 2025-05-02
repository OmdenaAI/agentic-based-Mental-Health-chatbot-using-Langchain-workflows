import sys 
import os
sys.path.append(os.path.abspath("src"))

import streamlit as st
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
from mentalhealth_chatbot.main import get_bot_response

# Load environment variables
load_dotenv()

# Page setup
st.set_page_config(page_title="MindfulChat - Let's Talk!", page_icon="💬")
st.title("MindfulChat - Let's Talk!")

if not os.getenv("SPEECH_KEY_PATH"):
    st.warning("Please set SPEECH_KEY_PATH in your .env file.")
    st.stop()

if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

engine = pyttsx3.init()

# Initial message
if len(st.session_state.conversation) == 0:
    intro = "Hi! I'm here to support you."
    if "completed_assessments" in st.session_state and st.session_state.completed_assessments:
        issues = ', '.join(st.session_state.completed_assessments)
        intro += f" Based on your completed assessments ({issues}), feel free to talk."
    else:
        intro += " How are you feeling today?"
    st.session_state.conversation.append(f"Bot: {intro}")

# Display chat history
for msg in st.session_state.conversation:
    if msg.startswith("User:"):
        st.markdown(f"👤 **You:** {msg[6:]}")
    elif msg.startswith("Bot:"):
        st.markdown(f"🤖 {msg[5:]}")

# Speech recognition function
def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("SPEECH_KEY_PATH")

    with mic as source:
        st.info("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            text = recognizer.recognize_google_cloud(audio)
            st.success(f"Recognized: {text}")
            return text
        except sr.WaitTimeoutError:
            st.warning("⏱️ Timeout. Try again.")
        except sr.UnknownValueError:
            st.warning("🤔 Didn't catch that. Speak clearly.")
        except sr.RequestError as e:
            st.error(f"❌ STT API Error: {e}")
        except Exception as e:
            st.error(f"⚠️ Unexpected error: {e}")
    return ""

# Input controls
cols = st.columns([10, 1, 1])
text_input = cols[0].text_input("Message", placeholder="Type or use mic...", label_visibility="collapsed", key="text_input_key")
send_clicked = cols[1].button("➤", key="send_button")
mic_clicked = cols[2].button("🎙️", key="mic_button")

# Handle mic input
if mic_clicked:
    st.session_state.user_input = recognize_speech_from_mic()
    st.rerun()

# Final input source
final_input = st.session_state.user_input if st.session_state.user_input else st.session_state.get("text_input_key", "")

# Get bot response
if (send_clicked and final_input) or st.session_state.user_input:
    with st.spinner("🤖 Thinking..."):
        history = st.session_state.conversation.copy()
        context = st.session_state.completed_assessments if "completed_assessments" in st.session_state else None
        bot_reply, updated_convo = get_bot_response(final_input, history, context=context)
        st.session_state.conversation = updated_convo

        if bot_reply:
            text_to_speak = bot_reply.final_output if hasattr(bot_reply, "final_output") else str(bot_reply)
            engine.say(text_to_speak[:400])  # Limit to 400 chars for now
            engine.runAndWait()

    st.session_state.user_input = ""
    st.rerun()
