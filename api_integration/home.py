import streamlit as st

st.set_page_config(
    page_title="Mental Health Chatbot",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("Mental Health Support Application")
st.markdown("""
### Welcome and thanks for taking the step towards your Mental Health!

This application is designed to provide supportive conversations through a structured process:

#### How it works:
1. **Step 1**: Provide your basic information
3. **Step 2**: Get personalized support based on your needs

Don't worry - you can take your time at each step.      
""")
#2. **Step 2**: Complete a therapy session with our AI therapist
# Add navigation button
if st.button("🚀 Get Started", type="primary"):
    #st.switch_page("pages/streamlit_app_copy.py")
    st.switch_page("pages/1_user_form.py")

# Add information about privacy and process
st.markdown("---")
st.markdown("""
### Your Privacy Matters
- All information is kept confidential
- You can choose what to share
- Our AI is designed to be supportive and non-judgmental
""")

#Add information about Technical implementation of the chatbot in sidebar
with st.sidebar:
        # Add information about next steps
        st.title("Technical Implementation Details")
        st.markdown("""
                    **Multi-Agent System:**
                    - **Assistant**: Empathetic listener who assesses mental state through logical conversation.
                    - **Summarizer**: Tracks conversations to provide concise summaries to the expert.
                    - **Expert**: Mental health professional delivering brief, evidence-based guidance from trusted sources.
                    
                    **Knowledge Base:**
                    For this demo, we use PDF documents containing mental health resources. The system searches these documents to find information relevant to your specific needs.
                    
                    **Memory System:**
                    We use Mem0 to maintain context throughout your session, ensuring personalized and coherent support.
        """)
#- **Therapist Agent**: Conducts structured interviews with empathetic questioning
#- **Knowledge Specialist**: Searches our mental health knowledge base for relevant information
#- **Summarizer Agent**: Creates personalized, actionable responses based on your context