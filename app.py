import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

from database import store_csv, run_query
from llm import generate_sql
from utils.schema_helper import get_schema
from explain_results import explain
from chart_generator import generate_chart


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


st.set_page_config(
    page_title="AI SQL Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI SQL Assistant")
st.markdown("Ask questions about your **CSV data in plain English**.")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:

    df = store_csv(uploaded_file)

    st.success("Dataset loaded successfully")

    st.subheader("Preview Data")
    st.dataframe(df.head())

    schema = get_schema(df)

    question = st.text_input("Ask your question")

    if question:

        with st.spinner("Generating SQL query..."):

            sql = generate_sql(question, schema)

        st.subheader("Generated SQL")

        st.code(sql, language="sql")

        result = run_query(sql)

        st.subheader("Query Result")

        st.dataframe(result)

        if len(result.columns) >= 2:

            st.subheader("Visualization")

            chart = generate_chart(result)

            st.plotly_chart(chart, use_container_width=True)

        st.subheader("Explanation")

        explanation = explain(question, result)

        st.write(explanation)