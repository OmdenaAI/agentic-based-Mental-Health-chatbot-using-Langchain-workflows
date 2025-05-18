# 4_Profile.py

import streamlit as st

st.set_page_config(page_title="Your Profile", page_icon="👤")

st.title("Your Profile")

# --- Check if all previous steps completed ---
required_keys = ["name", "age", "gender", "financial_status", "education", "generation", "mental_health_state", "mental_health_issues", "Consent Given"]
if not all(key in st.session_state.user_profile for key in required_keys):
    st.error("Please complete all previous steps first!")
    st.stop()

profile = st.session_state.user_profile

# --- Display Profile ---
st.write("### Name:", profile.get("name"))
st.write("### Age:", profile.get("age"))
st.write("### Gender:", profile.get("gender"))
st.write("### Financial Status:", profile.get("financial_status"))
st.write("### Education:", profile.get("education"))
st.write("### Generation:", profile.get("generation"))
st.write("### Mental Health State:", profile.get("mental_health_state"))

if profile.get("mental_health_issues"):
    st.write("### Mental Health Issues:")
    for issue in profile["mental_health_issues"]:
        st.markdown(f"- {issue}")

# --- Navigation ---
if st.button("Continue to Assessment Selection"):
    st.switch_page("pages/5_Assessment_Selection.py")

