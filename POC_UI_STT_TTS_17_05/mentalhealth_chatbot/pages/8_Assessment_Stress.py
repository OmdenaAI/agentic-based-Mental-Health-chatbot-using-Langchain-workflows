# 8_Assessment_Stress.py

import streamlit as st

st.set_page_config(page_title="Stress Assessment", page_icon="💥")

# --- Check if user has completed previous steps ---
if "mental_health_issues" not in st.session_state or not st.session_state.mental_health_issues:
    st.error("Please complete previous steps first!")
    st.stop()

if "Stress" not in st.session_state.mental_health_issues:
    st.error("Stress was not selected. Please go back and choose correct assessment.")
    st.stop()

# --- Initialize session states ---
if "stress_answers" not in st.session_state:
    st.session_state.stress_answers = []
if "assessment_page_stress" not in st.session_state:
    st.session_state.assessment_page_stress = 0
if "completed_assessments" not in st.session_state:
    st.session_state.completed_assessments = []

# --- PSS-5 Questions ---
questions = [
    "Been upset because of something that happened unexpectedly?",
    "Felt that you were unable to control the important things in your life?",
    "Felt nervous and stressed?",
    "Felt confident about your ability to handle your personal problems?",
    "Felt that things were going your way?"
]

options = ["Never", "Almost never", "Sometimes", "Fairly often", "Very often"]

score_mapping = {
    "Never": 0,
    "Almost never": 1,
    "Sometimes": 2,
    "Fairly often": 3,
    "Very often": 4
}

# --- UI Setup ---
st.title("💥 Stress Assessment (PSS-5)")
st.write("Please indicate how often you have felt or thought a certain way during the last month:")

current_q = st.session_state.assessment_page_stress

if current_q < len(questions):
    st.progress(current_q / len(questions))

    with st.form(key=f"stress_form_{current_q}"):
        selected_option = st.radio(questions[current_q], options, key=f"stress_q_{current_q}")

        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("⬅️ Back"):
                if st.session_state.assessment_page_stress > 0:
                    st.session_state.assessment_page_stress -= 1
                    st.session_state.stress_answers.pop()  # Remove last answer
                st.rerun()

        with col2:
            if st.form_submit_button("Next ➡️"):
                st.session_state.stress_answers.append(selected_option)
                st.session_state.assessment_page_stress += 1
                st.rerun()

else:
    # --- Calculate the stress score ---
    total_score = sum(score_mapping[ans] for ans in st.session_state.stress_answers)
    max_score = len(questions) * 4

    st.success(f"Score: {total_score} / {max_score}")

    percentage = (total_score / max_score) * 100

    if percentage < 33:
        meaning = "Low stress"
    elif percentage < 66:
        meaning = "Moderate stress"
    else:
        meaning = "High stress"

    st.info(f"Your responses suggest: **{meaning}**")

    # --- Save results ---
    st.session_state.stress_score = total_score
    st.session_state.stress_result = meaning

    if "Stress" not in st.session_state.completed_assessments:
        st.session_state.completed_assessments.append("Stress")

    st.success("✅ Stress Assessment completed!")

    # --- Navigation ---
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
