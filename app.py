import streamlit as st
import google.generativeai as genai

# 🔑 Set your Gemini API key
genai.configure(api_key="AIzaSyDrlfoVwUmCkPDy6K3rdeCWM20uisl3134")

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize session state
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "response" not in st.session_state:
    st.session_state.response = ""

# Streamlit UI
st.title("💬 Duvex-Powered AI Assistant")

with st.form(key="chat_form"):
    user_input = st.text_input("Type your message here:", value=st.session_state.user_input)
    submitted = st.form_submit_button("Send")

    if submitted and user_input:
        st.write("🤖 Thinking...")
        response = model.generate_content(user_input)
        st.session_state.response = response.text
        st.session_state.user_input = ""  # Clear input field

# Show response
if st.session_state.response:
    st.markdown(f"**Gemini says:** {st.session_state.response}")
