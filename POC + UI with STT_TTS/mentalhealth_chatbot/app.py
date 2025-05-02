import streamlit as st


# Page configuration
st.set_page_config(page_title="MindfulChat", page_icon="💬", layout="centered")

# Landing Page Content
st.markdown(
    """
    <div style="text-align: center;">
        <h1>MindfulChat</h1>
        <h4>A safe space to talk about your mental health</h4>
        <p>MindfulChat is here to provide support, resources, and a listening ear when you need it.</p>
        <br>
        <a href="/User_Info" target="_self">
            <button style="background-color: #2E8B57; color: white; padding: 10px 20px; font-size: 18px; border-radius: 8px;">Get Started</button>
        </a>
        <br><br>
        <p style="font-size: 12px;">Note: This is not a replacement for professional mental health services. If you are in crisis, please contact emergency services.</p>
    </div>
    """,
    unsafe_allow_html=True
)
