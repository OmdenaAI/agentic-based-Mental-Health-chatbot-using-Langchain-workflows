import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv
load_dotenv()

FASTAPI_BASE = "http://localhost:8000"

st.set_page_config(page_title="Mental Health Assistant", page_icon="🧠")

if "chat_started" not in st.session_state:
    st.session_state.chat_started = False
    st.session_state.name = ""
    st.session_state.messages = []
    st.session_state.feedback_log = []
    st.session_state.feedback_pending = False
    st.session_state.show_followup_prompt = False
    st.session_state.clear_input_flag = False
    st.session_state.show_input = True

st.title("🧠 Mental Health Assistant")

if not st.session_state.chat_started:
    with st.form(key="user_info_form"):
        st.subheader("👤 Tell us a bit about yourself")
        name = st.text_input("Your name:", value="")
        age = st.selectbox("Age group:", ["Under 18", "18-25", "26-35", "36-50", "51+"])
        gender = st.selectbox("Gender:", ["Female", "Male", "Non-binary", "Prefer not to say"])
        education = st.selectbox("Education level:", ["High school", "Bachelor", "Master", "PhD"])
        submitted = st.form_submit_button("Start Chat")

        if submitted:
            st.session_state.name = name
            st.session_state.chat_started = True
            st.success(f"Hi {name}, let’s begin. You can ask me anything related to mental health.")

if st.session_state.chat_started:
    st.markdown("---")
    st.subheader("💬 Ask a question or share your thoughts")

    if st.button("🎙️ Speak Your Question"):
        with st.spinner("Listening..."):
            try:
                r = requests.post(f"{FASTAPI_BASE}/speech-to-text")
                r.raise_for_status()
                result = r.json()
                user_query = result.get("transcription", "Sorry, no transcription received.")
            except requests.exceptions.RequestException as e:
                st.error(f"API error: {e}")
                user_query = "Sorry, I couldn't capture your voice."

        with st.spinner("Thinking..."):
            try:
                r = requests.post(f"{FASTAPI_BASE}/chat", json={"text": user_query})
                r.raise_for_status()
                result = r.json()
                response = result.get("response", "Sorry, no valid response received.")
            except requests.exceptions.RequestException as e:
                st.error(f"Error during chat API call: {e}")
                response = "Sorry, I had trouble generating a response."

    # 🔧 FIX: Append to messages for UI display
        st.session_state.messages.append(("user", user_query))
        st.session_state.messages.append(("bot", response))
        st.session_state.latest_query = user_query
        st.session_state.latest_response = response
        st.session_state.feedback_pending = True

    # Optional: Text-to-speech output
        requests.post(f"{FASTAPI_BASE}/text-to-speech", json={"text": response})

        st.success("Response received!")


    if st.session_state.show_input:
        if st.session_state.clear_input_flag:
            user_query = st.text_input("You:", key="user_input", value="")
            st.session_state.clear_input_flag = False
        else:
            user_query = st.text_input("You:", key="user_input")

        if user_query and (not st.session_state.feedback_pending):
            st.session_state.messages.append(("user", user_query))

            with st.spinner("Thinking..."):
                r = requests.post(f"{FASTAPI_BASE}/chat", json={"text": user_query})
                response = r.json()["response"]
                st.session_state.messages.append(("bot", response))
                requests.post(f"{FASTAPI_BASE}/text-to-speech", json={"text": response})
                st.session_state.latest_query = user_query
                st.session_state.latest_response = response
                st.session_state.feedback_pending = True

            st.success("Response received!")

    for role, msg in st.session_state.messages:
        if role == "user":
            st.markdown(f"👩 **You:** {msg}")
        else:
            st.markdown(f"🧠 **Assistant:** {msg}")

    if st.session_state.feedback_pending:
        st.markdown("---")
        st.subheader("📣 Was this response helpful?")
        rating = st.radio("Rate the response:", ("👍 Yes", "👎 No"), horizontal=True, key="rating")
        comment = st.text_area("Any suggestions or comments?", key="comment")

        if st.button("Submit Feedback"):
            st.session_state.feedback_log.append({
                "name": st.session_state.name,
                "query": st.session_state.latest_query,
                "response": st.session_state.latest_response,
                "rating": rating,
                "comment": comment
            })
            pd.DataFrame(st.session_state.feedback_log).to_csv("feedback_log.csv", index=False)

            if rating == "👍 Yes":
                st.session_state.followup_message = "✅ Thank you! Ready when you are to ask your next question."
            else:
                st.session_state.followup_message = "🙏 Thanks! Feel free to clarify or continue the conversation above."

            st.session_state.feedback_pending = False
            st.session_state.show_followup_prompt = True
            st.session_state.show_input = False

    if st.session_state.get("show_followup_prompt", False):
        st.markdown("---")
        st.info(st.session_state.followup_message)

        if st.button("➡️ Continue", key="continue_button"):
            st.session_state.show_followup_prompt = False
            st.session_state.clear_input_flag = True
            st.session_state.show_input = True
            st.rerun()
