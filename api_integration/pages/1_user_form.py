import streamlit as st
import sys
import os
from dotenv import load_dotenv

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

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
if "user_data" not in st.session_state:
    st.session_state.user_data = False
if "page" not in st.session_state:
    st.session_state.page = "info"

# Create sidebar content
with st.sidebar:
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    # Add information about next steps
    st.title("What Happens Next?")
    st.markdown("""
                    After you submit this form, you'll proceed to:
                    
                    **Support Chat**: You'll have access to personalized support based on your complete profile
                    All information is used to provide more relevant and helpful support.
        """)
    # 1. **Therapy Session**: Our AI therapist will ask you a few questions to better understand your situation
    st.markdown("</div>", unsafe_allow_html=True)

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
    if progress == 100 and st.button("✅ Submit and Start Chat"):
        st.session_state.user_data = {
            "name": name, "age": age, "gender": gender, "occupation": occupation}
        st.session_state.page = "chat"
        st.switch_page("pages/3_chatbot.py")  # Navigate to chatbot page

# Main execution
if __name__ == "__main__":
    if st.session_state.page == "info" or not st.session_state.user_data:
        collect_user_info()
    else:
        # If user data exists but we're still on this page, redirect to chatbot
        st.switch_page("pages/3_chatbot.py")