# 9_Assessment_FOMO.py

import streamlit as st

st.set_page_config(page_title="FOMO Assessment", page_icon="📱")

# --- Check if user has completed previous steps ---
if "mental_health_issues" not in st.session_state or not st.session_state.mental_health_issues:
    st.error("Please complete previous steps first!")
    st.stop()

if "Social Media FOMO" not in st.session_state.mental_health_issues:
    st.error("Social Media FOMO was not selected. Please go back and choose correct assessment.")
    st.stop()

# --- Initialize session state ---
if "fomo_answers" not in st.session_state:
    st.session_state.fomo_answers = []
if "completed_assessments" not in st.session_state:
    st.session_state.completed_assessments = []

# --- FOMO Assessment Questions ---
questions = [
    "I fear others have more rewarding experiences than me.",
    "I fear my friends have more rewarding lives than me.",
    "I get worried when I find out my friends are having fun without me.",
    "I get anxious when I don’t know what my friends are up to.",
    "Sometimes I wonder if I spend too much time keeping up with what’s going on."
]

options = ["Not at all true", "Slightly true", "Moderately true", "Very true", "Extremely true"]

score_mapping = {
    "Not at all true": 0,
    "Slightly true": 1,
    "Moderately true": 2,
    "Very true": 3,
    "Extremely true": 4
}

st.title("📱 Social Media FOMO Assessment")
st.write("Please indicate how much the following statements apply to you:")

current_q = len(st.session_state.fomo_answers)

if current_q < len(questions):
    st.progress(current_q / len(questions))
    answer = st.radio(questions[current_q], options)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            if current_q > 0:
                st.session_state.fomo_answers.pop()
                st.rerun()

    with col2:
        if st.button("Next"):
            st.session_state.fomo_answers.append(answer)
            st.rerun()
else:
    # --- Calculate the FOMO score ---
    total_score = sum(score_mapping[ans] for ans in st.session_state.fomo_answers)
    max_score = len(questions) * 4

    st.success(f"Score: {total_score} / {max_score}")

    percentage = (total_score / max_score) * 100

    if percentage < 33:
        meaning = "Low FOMO tendencies"
    elif percentage < 66:
        meaning = "Moderate FOMO tendencies"
    else:
        meaning = "High FOMO tendencies"

    st.info(f"Your responses suggest: {meaning}")

    # --- Save to session_state ---
    st.session_state.fomo_score = total_score
    st.session_state.fomo_result = meaning

    if "Social Media FOMO" not in st.session_state.completed_assessments:
        st.session_state.completed_assessments.append("Social Media FOMO")

    st.success("FOMO Assessment completed!")

    # --- Navigation options ---
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Profile"):
            st.switch_page("pages/4_Profile.py")
    with col2:
        if st.button("Continue Assessment / Chat"):
            # Check if any assessments pending
            pending = [issue for issue in st.session_state.mental_health_issues if issue not in st.session_state.completed_assessments]
            if pending:
                st.switch_page("pages/5_Assessment_Selection.py")
            else:
                st.switch_page("pages/10_Chat.py")
