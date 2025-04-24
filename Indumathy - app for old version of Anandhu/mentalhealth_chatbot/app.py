import sys
import os
sys.path.append(os.path.abspath("src"))

import streamlit as st
from dotenv import load_dotenv
from mentalhealth_chatbot.main import get_bot_response


# Load environment variables
load_dotenv()

# Page setup
st.set_page_config(page_title="Mental Health Chatbot", page_icon="🤖")
st.title("🤖 Mental Health Chatbot")

# Environment key check
if not os.getenv("GOOGLE_API_KEY"):
    st.warning("Please set your GOOGLE_API_KEY in a .env file before using the chatbot.")
    st.stop()

# Session memory
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Input field
user_input = st.text_input("How are you feeling today?", key="user_input")

# Get response
if user_input:
    with st.spinner("Thinking..."):
        bot_reply, st.session_state.conversation = get_bot_response(user_input, st.session_state.conversation)
        st.session_state.conversation.append(f"Bot: {bot_reply}")

# Display only latest bot reply
if st.session_state.conversation:
    last_msg = st.session_state.conversation[-1]
    if last_msg.startswith("Bot:"):
        st.markdown(f"🤖 **Bot:** {last_msg[5:]}")