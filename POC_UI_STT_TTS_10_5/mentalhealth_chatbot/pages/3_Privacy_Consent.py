# --- 3_Privacy_Consent.py (FINAL FIXED VERSION) ---
import streamlit as st

# Page setup
st.set_page_config(page_title="Privacy & Consent", page_icon="🔒")
st.title("User Information")
st.subheader("Step 3 of 3: Privacy & Consent")

# Progress Bar
st.progress(3/3)

# Privacy Notice
st.markdown("""
<div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px;'>
    <h4>Privacy & Data Usage</h4>
    <p>MindfulChat values your privacy. Your conversations are encrypted and stored securely. 
    We use anonymized data to improve our service and provide better support.
    You can request deletion of your data at any time.</p>
</div>
""", unsafe_allow_html=True)

# --- Initialize session ---
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}

# Consent Checkbox
consent = st.checkbox("I consent to the storage and processing of my data as described in the privacy policy. I understand that MindfulChat is not a replacement for professional mental health services.")

# --- Submit Button ---
if st.button("Submit"):
    if consent:
        st.session_state.user_profile["Consent Given"] = True
        st.success("Thank you for your consent! Your profile is ready.")
        st.session_state.mental_health_issues = st.session_state.user_profile.get("Mental Health Issues", [])

        # Initialize assessment tracking
        #st.session_state.completed_assessments = []

        st.switch_page("pages/5_Assessment_Selection.py")
    else:
        st.error("You must give consent to proceed.")
