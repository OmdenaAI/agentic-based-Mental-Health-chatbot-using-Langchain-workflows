import streamlit as st

# Ensure user_profile exists
if "user_profile" not in st.session_state:
    st.error("Please complete Step 1 first!")
    st.stop()

# Page
st.title("User Information")
st.subheader("Step 2 of 3: Mental Health")

# Form for mental health information
with st.form(key="mental_health_form"):
    mental_health_issues = st.multiselect(
        "Mental Health Issues (select all that apply):",
        options=["Depression", "Anxiety", "Stress", "Social Media FOMO"]
    )
    mental_health_state = st.selectbox(
        "Current Mental Health State",
        options=["Excellent", "Good", "Fair", "Poor", "At Risk", "In Crisis"]
    )
    submit = st.form_submit_button("Next")

if submit:
    # Save to session
    st.session_state.user_profile.update({
        "Mental Health Issues": mental_health_issues,
        "Current Mental Health State": mental_health_state
    })
    st.success("Mental health info saved! Please proceed to the next step.")
    st.switch_page("pages/3_Privacy_Consent.py")
