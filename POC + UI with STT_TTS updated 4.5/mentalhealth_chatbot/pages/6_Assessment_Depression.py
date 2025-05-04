# 6_Assessment_Depression.py

import streamlit as st

st.set_page_config(page_title="Depression Assessment", page_icon="😔")

# --- Check if user has completed previous steps ---
if "mental_health_issues" not in st.session_state or not st.session_state.mental_health_issues:
    st.error("Please complete previous steps first!")
    st.stop()

if "Depression" not in st.session_state.mental_health_issues:
    st.error("Depression was not selected. Please go back and choose correct assessment.")
    st.stop()

# --- Initialize session state ---
if "depression_answers" not in st.session_state:
    st.session_state.depression_answers = []
if "completed_assessments" not in st.session_state:
    st.session_state.completed_assessments = []

# --- PHQ-9 Questions for Depression ---
questions = [
    "Little interest or pleasure in doing things?",
    "Feeling down, depressed, or hopeless?",
    "Trouble falling or staying asleep, or sleeping too much?",
    "Feeling tired or having little energy?",
    "Poor appetite or overeating?"
]

options = ["Not at all", "Several days", "More than half the days", "Nearly every day"]

score_mapping = {
    "Not at all": 0,
    "Several days": 1,
    "More than half the days": 2,
    "Nearly every day": 3
}

st.title("🧠 Depression Assessment (PHQ-9)")
st.write("Please indicate how often you have been bothered by the following problems over the past 2 weeks:")

current_q = len(st.session_state.depression_answers)

if current_q < len(questions):
    st.progress(current_q / len(questions))
    answer = st.radio(questions[current_q], options)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Back"):
            st.switch_page("pages/5_Assessment_Selection.py")
    with col2:
        if st.button("Next"):
            st.session_state.depression_answers.append(answer)
            st.rerun()
else:
    # --- Calculate the depression score ---
    total_score = sum(score_mapping[ans] for ans in st.session_state.depression_answers)
    max_score = len(questions) * 3

    st.success(f"Score: {total_score} / {max_score}")

    if total_score <= 4:
        meaning = "Minimal depression"
    elif total_score <= 9:
        meaning = "Mild depression"
    elif total_score <= 14:
        meaning = "Moderate depression"
    else:
        meaning = "Severe depression"

    st.info(f"Your responses suggest: {meaning}")

    # --- Save to session_state ---
    st.session_state.depression_score = total_score
    st.session_state.depression_result = meaning

    if "Depression" not in st.session_state.completed_assessments:
        st.session_state.completed_assessments.append("Depression")

    st.success("Depression Assessment completed!")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back to Profile"):
            st.switch_page("pages/4_Profile.py")
    with col2:
        if st.button("Continue Assessment / Chat"):
            pending = [issue for issue in st.session_state.mental_health_issues if issue not in st.session_state.completed_assessments]
            if pending:
                st.switch_page("pages/5_Assessment_Selection.py")
            else:
                st.switch_page("pages/10_Chat.py")
