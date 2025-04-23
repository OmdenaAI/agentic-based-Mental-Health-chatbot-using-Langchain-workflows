import streamlit as st
# Adjust the import based on your project structure
import sys
import os

# Add the current directory to the Python path if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Try alternative import paths - uncomment the one that works
# Import approach 1: If your main file is in src/crewai_knowledge_chatbot/crew.py
from src.crewai_knowledge_chatbot.crew import CrewaiKnowledgeChatbot

# Import approach 2: If your main file is at the root level
# from crew import CrewaiKnowledgeChatbot
import os
from dotenv import load_dotenv
import time

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
}
.chat-message.assistant {
    background-color: #e3f2fd;
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

# Create sidebar content
with st.sidebar:
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    st.title("Chatbot details")
    st.markdown("### About")
    st.markdown("This chatbot uses CrewAI and Mem0 to provide context-aware responses using the knowledge from the PDF document. It uses Streamlit for the UI.")
    
    # Display document info
    st.markdown("### PDF Information")
    st.markdown("<div class='document-info'>", unsafe_allow_html=True)
    st.markdown("📄 **Loaded Document**: CoALA.pdf")
    st.markdown("**Title**: Cognitive Architectures for Language Agents")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# Display chat messages
st.title("Mental Health Chatbot 🤖")

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
user_input = st.chat_input("How are you feeling today?")

# Process user input
if user_input:
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_input})
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
    st.session_state.messages.append({"role": "assistant", "content": response})
    
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
    st.rerun()

# Add a footer
st.markdown("---")
st.markdown("Powered by CrewAI and Mem0 | Built with Streamlit")