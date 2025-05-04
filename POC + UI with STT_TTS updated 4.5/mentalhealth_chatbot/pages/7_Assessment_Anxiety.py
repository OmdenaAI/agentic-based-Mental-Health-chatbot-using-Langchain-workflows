import streamlit as st

st.set_page_config(page_title="Anxiety Assessment", page_icon="😟")

# --- Pre-check ---
if "mental_health_issues" not in st.session_state or "Anxiety" not in st.session_state.mental_health_issues:
    st.error("Please complete previous steps and ensure 'Anxiety' is selected.")
    st.stop()

# --- Initialize session ---
if "anxiety_answers" not in st.session_state:
    st.session_state.anxiety_answers = []
if "completed_assessments" not in st.session_state:
    st.session_state.completed_assessments = []

# --- GAD-7 Questions ---
questions = [
    "Feeling nervous, anxious, or on edge?",
    "Not being able to stop or control worrying?",
    "Worrying too much about different things?",
    "Trouble relaxing?",
    "Being so restless that it is hard to sit still?",
    "Becoming easily annoyed or irritable?",
    "Feeling afraid as if something awful might happen?"
]

options = ["Not at all", "Several days", "More than half the days", "Nearly every day"]
score_mapping = {
    "Not at all": 0,
    "Several days": 1,
    "More than half the days": 2,
    "Nearly every day": 3
}

st.title("🌩️ Anxiety Assessment (GAD-7)")
st.write("Over the last 2 weeks, how often have you been bothered by the following problems:")

current_q = len(st.session_state.anxiety_answers)

if current_q < len(questions):
    st.progress(current_q / len(questions))
    answer = st.radio(questions[current_q], options)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back") and current_q > 0:
            st.session_state.anxiety_answers.pop()
            st.rerun()
    with col2:
        if st.button("➡️ Next"):
            st.session_state.anxiety_answers.append(answer)
            st.rerun()
else:
    # --- Score Evaluation ---
    total_score = sum(score_mapping[ans] for ans in st.session_state.anxiety_answers)
    max_score = len(questions) * 3

    st.success(f"Score: {total_score} / {max_score}")

    if total_score <= 5:
        meaning = "Minimal anxiety"
    elif total_score <= 10:
        meaning = "Mild anxiety"
    elif total_score <= 15:
        meaning = "Moderate anxiety"
    else:
        meaning = "Severe anxiety"

    st.info(f"Your responses indicate: **{meaning}**")

    # --- Save and redirect ---
    st.session_state.anxiety_score = total_score
    st.session_state.anxiety_result = meaning

    if "Anxiety" not in st.session_state.completed_assessments:
        st.session_state.completed_assessments.append("Anxiety")

    st.success("Anxiety Assessment completed!")

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
