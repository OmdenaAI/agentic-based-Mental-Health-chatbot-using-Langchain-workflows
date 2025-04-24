# ==================================================
# 🧠 Streamlit UI: Mental Health Assistant (POC v1)
# - Chat interface with supportive responses via Groq RAG
# - User feedback handling and CSV export
# - Modular with `agents.py` (LLM logic) and `rag_pipeline.py`
#
# ✅ Improvements over time:
#   - Memory-aware conversations
#   - Feedback-informed refinement
#   - Optional agent workflows and routing logic
# ==================================================

import streamlit as st
import pandas as pd
import os
#from autogen_LlamaIndex import ensure_index_exists
from dotenv import load_dotenv
load_dotenv()
from autogen_LlamaIndex import handle_user_query
# ==================================================
# ✅ Ensure Vector Index Exists (Only on First Launch)
# ==================================================
#ensure_index_exists()
os.environ["TORCH_USE_RTLD_GLOBAL"] = "YES"
# === Configure Streamlit page ===
st.set_page_config(page_title="Mental Health Assistant", page_icon="🧠")

# ==================================================
# 🧠 Session State Initialization
# ==================================================
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False
    st.session_state.name = ""
    st.session_state.messages = []
    st.session_state.feedback_log = []
    st.session_state.feedback_pending = False
    st.session_state.show_followup_prompt = False
    st.session_state.clear_input_flag = False
    st.session_state.show_input = True

# ==================================================
# 🧠 Title & User Info Form
# ==================================================
st.title("🧠 Mental Health Assistant")

if not st.session_state.chat_started:
    with st.form(key="user_info_form"):
        st.subheader("👤 Tell us a bit about yourself")
        name = st.text_input("Your name:", value="Sara")
        age = st.selectbox("Age group:", ["Under 18", "18-25", "26-35", "36-50", "51+"])
        gender = st.selectbox("Gender:", ["Female", "Male", "Non-binary", "Prefer not to say"])
        education = st.selectbox("Education level:", ["High school", "Bachelor", "Master", "PhD"])
        submitted = st.form_submit_button("Start Chat")

        if submitted:
            st.session_state.name = name
            st.session_state.chat_started = True
            st.success(f"Hi {name}, let’s begin. You can ask me anything related to mental health.")

# ==================================================
# 💬 Chat Interface
# ==================================================
if st.session_state.chat_started:
    st.markdown("---")
    st.subheader("💬 Ask a question or share your thoughts")

    if st.session_state.show_input:
        if st.session_state.clear_input_flag:
            user_query = st.text_input("You:", key="user_input", value="")
            st.session_state.clear_input_flag = False
        else:
            user_query = st.text_input("You:", key="user_input")

        if user_query and (not st.session_state.feedback_pending):
            st.session_state.messages.append(("user", user_query))

            with st.spinner("Thinking..."):
                response = handle_user_query(user_query)
                st.session_state.messages.append(("bot", response))
                st.session_state.latest_query = user_query
                st.session_state.latest_response = response
                st.session_state.feedback_pending = True

            st.success("Response received!")

    # === Display messages ===
    for role, msg in st.session_state.messages:
        if role == "user":
            st.markdown(f"👩 **You:** {msg}")
        else:
            st.markdown(f"🧠 **Assistant:** {msg}")

    # ==================================================
    # 📣 Feedback Section
    # ==================================================
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

    # ==================================================
    # ➕ Follow-up Prompt
    # ==================================================
    if st.session_state.get("show_followup_prompt", False):
        st.markdown("---")
        st.info(st.session_state.followup_message)

        if st.button("➡️ Continue", key="continue_button"):
            st.session_state.show_followup_prompt = False
            st.session_state.clear_input_flag = True
            st.session_state.show_input = True
            st.rerun()
