# 5_Assessment_Selection.py

import streamlit as st

# Set page configuration
st.set_page_config(page_title="Assessment Selection", page_icon="📝")

st.title("Assessment Selection")
st.subheader("Select an assessment based on your reported mental health issues:")

# Check if the user has completed previous steps
if "mental_health_issues" not in st.session_state or not st.session_state.mental_health_issues:
    st.error("Please complete previous steps first!")
    st.stop()

# Initialize completed assessments if not already done
if "completed_assessments" not in st.session_state:
    st.session_state.completed_assessments = []

# Mapping of mental health issues to page files
issue_mapping = {
    "Depression": ("6_Assessment_Depression", "Depression Assessment", "❤️"),
    "Anxiety": ("7_Assessment_Anxiety", "Anxiety Assessment", "💛"),
    "Stress": ("8_Assessment_Stress", "Stress Assessment", "🧡"),
    "Social Media FOMO": ("9_Assessment_FOMO", "Social Media FOMO Assessment", "💙"),
}

# Display each assessment card
for issue in st.session_state.mental_health_issues:
    if issue in issue_mapping:
        page_name, description, emoji = issue_mapping[issue]
        with st.container():
            st.markdown(f"### {emoji} {description}")
            st.markdown(f"*Assessment related to {issue}*")
            
            if issue in st.session_state.completed_assessments:
                st.success("✅ Completed")
                if st.button(f"Retake {issue} Assessment", key=f"retake_{issue}"):
                    st.switch_page(f"pages/{page_name}.py")
            else:
                st.warning("🚧 Not completed yet")
                if st.button(f"Start {issue} Assessment", key=f"start_{issue}"):
                    st.switch_page(f"pages/{page_name}.py")

st.divider()

# Navigation options
col1, col2 = st.columns(2)

with col1:
    st.button("🔙 Back to Profile", on_click=lambda: st.switch_page("pages/4_Profile.py"))

with col2:
    if len(st.session_state.completed_assessments) > 0:
        st.button("💬 Continue to Chat", on_click=lambda: st.switch_page("pages/10_Chat.py"))
    else:
        st.button("💬 Continue to Chat (Disabled)", disabled=True)
