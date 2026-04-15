import streamlit as st
import pandas as pd
import os
import time
from dotenv import load_dotenv
import speech_recognition as sr
from io import BytesIO

from database import store_csv, run_query
from llm import generate_sql
from utils.schema_helper import get_schema
from explain_results import explain
from chart_generator import generate_chart

load_dotenv()

# ---------------------------
# Config
# ---------------------------
st.set_page_config(
    page_title="AI SQL Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------
# CSS (Enhanced + Chat UI)
# ---------------------------
st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

/* Title */
h1 {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(90deg, #4f46e5, #22c55e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Cards */
.card {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 20px;
    box-shadow: 0px 6px 25px rgba(0,0,0,0.4);
}

/* Section Titles */
.section-title {
    font-size: 22px;
    font-weight: 600;
    color: #22c55e;
    margin-bottom: 10px;
}

/* Inputs */
.stTextInput>div>div>input {
    background-color: #020617;
    color: white;
    border-radius: 12px;
    padding: 10px;
}

/* File uploader */
.stFileUploader {
    border: 2px dashed #4f46e5;
    padding: 20px;
    border-radius: 12px;
    background-color: #020617;
}

/* Chat bubbles */
.user-bubble {
    align-self: flex-end;
    background: #4f46e5;
    padding: 12px;
    border-radius: 12px;
    margin: 5px;
    color: white;
    max-width: 70%;
}

.ai-bubble {
    align-self: flex-start;
    background: #1e293b;
    padding: 12px;
    border-radius: 12px;
    margin: 5px;
    color: white;
    max-width: 70%;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #020617;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# Session State
# ---------------------------
if "datasets" not in st.session_state:
    st.session_state.datasets = {}

if "history" not in st.session_state:
    st.session_state.history = []

if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.title("📂 Data + History")

files = st.sidebar.file_uploader(
    "Upload CSV files",
    type=["csv"],
    accept_multiple_files=True
)

if files:
    for file in files:
        df = store_csv(file)
        st.session_state.datasets[file.name] = df

dataset_name = st.sidebar.selectbox(
    "Select Dataset",
    list(st.session_state.datasets.keys())
) if st.session_state.datasets else None

st.sidebar.subheader("🕘 History")
for q in st.session_state.history[::-1]:
    st.sidebar.write("•", q)

# ---------------------------
# Header
# ---------------------------
st.markdown("<h1>🤖 AI SQL Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Chat with your data like ChatGPT</p>", unsafe_allow_html=True)

# ---------------------------
# Voice Input
# ---------------------------
def voice_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening...")
        audio = r.listen(source)
        try:
            return r.recognize_google(audio)
        except:
            return ""

# ---------------------------
# Streaming Effect
# ---------------------------
def stream_text(text):
    for char in text:
        yield char
        time.sleep(0.01)

# ---------------------------
# Upload Card
# ---------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📂 Upload Dataset</div>', unsafe_allow_html=True)
st.write("Upload CSVs from sidebar and select dataset")
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# Main App
# ---------------------------
if dataset_name:

    df = st.session_state.datasets[dataset_name]

    # Preview
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Data Preview</div>', unsafe_allow_html=True)
    st.dataframe(df.head())
    st.markdown('</div>', unsafe_allow_html=True)

    schema = get_schema(df)

    # ---------------------------
    # Chat Section
    # ---------------------------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💬 Chat</div>', unsafe_allow_html=True)

    # Display chat history
    for msg in st.session_state.chat:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-bubble">{msg["content"]}</div>', unsafe_allow_html=True)

    # Input + Voice
    col1, col2 = st.columns([4,1])

    with col1:
        question = st.text_input("Ask your question")

    with col2:
        if st.button("🎙️"):
            question = voice_to_text()
            st.write("You said:", question)

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------
    # Chat Logic
    # ---------------------------
    if question:

        st.session_state.history.append(question)
        st.session_state.chat.append({"role": "user", "content": question})

        st.markdown(f'<div class="user-bubble">{question}</div>', unsafe_allow_html=True)

        with st.spinner("⚡ Thinking..."):
            sql = generate_sql(question, schema)
            result = run_query(sql)
            explanation = explain(question, result)

            full_response = f"""
<b>🧾 SQL:</b><br>{sql}<br><br>
<b>🧠 Explanation:</b><br>{explanation}
"""

        # Streaming AI response
        placeholder = st.empty()
        ai_text = ""

        for chunk in stream_text(full_response):
            ai_text += chunk
            placeholder.markdown(
                f'<div class="ai-bubble">{ai_text}</div>',
                unsafe_allow_html=True
            )

        st.session_state.chat.append({"role": "assistant", "content": full_response})

        # ---------------------------
        # Results Section
        # ---------------------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📌 Results</div>', unsafe_allow_html=True)
        st.dataframe(result)
        st.markdown('</div>', unsafe_allow_html=True)

        # Download
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">⬇️ Download</div>', unsafe_allow_html=True)

        csv = result.to_csv(index=False).encode()
        st.download_button("Download CSV", csv, "result.csv")

        buffer = BytesIO()
        result.to_excel(buffer, index=False)
        st.download_button("Download Excel", buffer.getvalue(), "result.xlsx")

        st.markdown('</div>', unsafe_allow_html=True)

        # Chart
        if len(result.columns) >= 2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📈 Visualization</div>', unsafe_allow_html=True)
            chart = generate_chart(result)
            st.plotly_chart(chart, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Insights
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🤖 Auto Insights</div>', unsafe_allow_html=True)

        numeric_cols = result.select_dtypes(include='number')

        if not numeric_cols.empty:
            for col in numeric_cols.columns:
                st.write(f"🔢 Avg {col}: {result[col].mean():.2f}")
                st.write(f"📈 Max {col}: {result[col].max()}")
                st.write(f"📉 Min {col}: {result[col].min()}")
        else:
            st.write("No numeric insights")

        st.markdown('</div>', unsafe_allow_html=True)
