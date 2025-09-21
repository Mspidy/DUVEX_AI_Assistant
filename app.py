import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import google.generativeai as genai
import io

# 🔑 Gemini API setup
genai.configure(api_key="AIzaSyDrlfoVwUmCkPDy6K3rdeCWM20uisl3134")
model = genai.GenerativeModel("gemini-1.5-flash")

# Session state init
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "response" not in st.session_state:
    st.session_state.response = ""

# 🌟 Section 1: Gemini Assistant
st.set_page_config(page_title="Duvex AI Assistant", layout="centered")
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
    st.markdown(f"<div style='background-color:#f0f2f6; padding:15px; border-radius:10px;'>"
                f"<strong>Gemini says:</strong><br>{st.session_state.response}</div>", unsafe_allow_html=True)

st.markdown("---")

# 📊 Section 2: Excel Upload + Dashboard
st.header("📈 Upload Excel & Generate Dashboard")

uploaded_file = st.file_uploader("Upload your Excel or CSV file", type=["xlsx", "xls", "csv"])
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
        y_axes = st.multiselect("Select one or more Y-axis columns", columns)

        graph_type = st.radio("Choose graph type", ["Line", "Bar", "Scatter", "Pie", "Radar"])

        if x_axis and y_axes:
            st.subheader("📊 Generated Graphs")
            for y in y_axes:
                fig, ax = plt.subplots()

                if graph_type == "Line":
                    ax.plot(df[x_axis], df[y], marker='o')
                elif graph_type == "Bar":
                    ax.bar(df[x_axis], df[y])
                elif graph_type == "Scatter":
                    ax.scatter(df[x_axis], df[y])
                elif graph_type == "Pie":
                    pie_data = df[y].value_counts()
                    fig, ax = plt.subplots()
                    ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
                    ax.set_title(f"{y} Distribution")
                elif graph_type == "Radar":
                    categories = df[x_axis].astype(str).tolist()
                    values = df[y].tolist()
                    angles = [n / float(len(categories)) * 2 * 3.14159 for n in range(len(categories))]
                    values += values[:1]
                    angles += angles[:1]

                    fig = plt.figure(figsize=(6, 6))
                    ax = plt.subplot(111, polar=True)
                    ax.plot(angles, values, marker='o')
                    ax.fill(angles, values, alpha=0.25)
                    ax.set_xticks(angles[:-1])
                    ax.set_xticklabels(categories)
                    ax.set_title(f"{y} Radar Chart")

                st.pyplot(fig)

                # 📥 Download graph as PNG
                buf = io.BytesIO()
                fig.savefig(buf, format="png")
                st.download_button(
                    label=f"📥 Download '{y} vs {x_axis}' Graph",
                    data=buf.getvalue(),
                    file_name=f"{y}_vs_{x_axis}_{graph_type}.png",
                    mime="image/png"
                )

            # 📥 Download selected data as CSV
            selected_data = df[[x_axis] + y_axes]
            csv_data = selected_data.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Selected Data as CSV",
                data=csv_data,
                file_name="selected_data.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
