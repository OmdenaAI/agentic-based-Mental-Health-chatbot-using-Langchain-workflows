import streamlit as st

# Initialize session state
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}

# Page
st.title("User Information")
st.subheader("Step 1 of 3: Personal Information")

# Form for user personal information
with st.form(key="user_info_form"):
    name = st.text_input("Name / Nickname (can be anonymous)", placeholder="How would you like to be called?")
    age_group = st.selectbox(
        "Age",
        options=["Under 18", "18-24", "25-34", "35-44", "45+"]
    )
    gender = st.radio(
        "Gender (optional)",
        options=["Male", "Female", "Non-binary", "Prefer not to say"]
    )
    financial_status = st.selectbox(
        "Financial Status",
        options=["Student", "Employed", "Self-employed", "Unemployed", "Retired", "Prefer not to say"]
    )
    education_level = st.selectbox(
        "Education",
        options=["High school", "Some college", "Bachelor's degree", "Master's degree", "Doctorate", "Other"]
    )
    generation = st.selectbox(
        "Generation",
        options=["Gen Z (1997-2012)", "Millennial (1981-1996)", "Gen X (1965-1980)", "Baby Boomer (1946-1964)", "Other"]
    )

    submit = st.form_submit_button("Next")

if submit:
    # Save data to session state
    st.session_state.user_profile.update({
        "Name": name if name else "Anonymous",
        "Age Group": age_group,
        "Gender": gender,
        "Financial Status": financial_status,
        "Education": education_level,
        "Generation": generation
    })
    st.success("Information saved! Please proceed to the next step.")
    st.switch_page("pages/2_Mental_Health.py")
