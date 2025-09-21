# import streamlit as st
# import google.generativeai as genai

# # 🔑 Set your Gemini API key
# genai.configure(api_key="AIzaSyDrlfoVwUmCkPDy6K3rdeCWM20uisl3134")

# # Load Gemini model
# model = genai.GenerativeModel("gemini-1.5-flash")

# # Initialize session state
# if "user_input" not in st.session_state:
#     st.session_state.user_input = ""
# if "response" not in st.session_state:
#     st.session_state.response = ""

# # Streamlit UI
# st.title("💬 Duvex-Powered AI Assistant")

# with st.form(key="chat_form"):
#     user_input = st.text_input("Type your message here:", value=st.session_state.user_input)
#     submitted = st.form_submit_button("Send")

#     if submitted and user_input:
#         st.write("🤖 Thinking...")
#         response = model.generate_content(user_input)
#         st.session_state.response = response.text
#         st.session_state.user_input = ""  # Clear input field

# # Show response
# if st.session_state.response:
#     st.markdown(f"**Gemini says:** {st.session_state.response}")


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai

# 🔑 Gemini API setup
genai.configure(api_key="AIzaSyDrlfoVwUmCkPDy6K3rdeCWM20uisl3134")
model = genai.GenerativeModel("gemini-1.5-flash")

# Session state init
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "response" not in st.session_state:
    st.session_state.response = ""

# 🌟 Section 1: Gemini Assistant
st.title("💬 Duvex-Powered AI Assistant")

with st.form(key="chat_form"):
    user_input = st.text_input("Type your message here:", value=st.session_state.user_input)
    submitted = st.form_submit_button("Send")

    if submitted and user_input:
        with st.spinner("🤖 Thinking..."):
            response = model.generate_content(user_input)
            st.session_state.response = response.text
            st.session_state.user_input = ""

if st.session_state.response:
    st.markdown(f"**Gemini says:** {st.session_state.response}")

st.markdown("---")

# 📊 Section 2: Excel Upload + Dashboard
st.header("📈 Upload Excel & Generate Dashboard")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls", "csv"])
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ File uploaded successfully!")
        st.dataframe(df.head())

        # Column selection
        st.subheader("🔧 Select Columns for Graph")
        columns = df.columns.tolist()
        x_axis = st.selectbox("Select X-axis column", columns)
        y_axis = st.selectbox("Select Y-axis column", columns)

        # Graph generation
        if x_axis and y_axis:
            st.subheader("📊 Generated Graph")
            fig, ax = plt.subplots()
            ax.plot(df[x_axis], df[y_axis], marker='o')
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            ax.set_title(f"{y_axis} vs {x_axis}")
            st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
