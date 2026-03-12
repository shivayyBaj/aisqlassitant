<<<<<<< HEAD

# 🤖 AI SQL Assistant

## 📌 Overview

AI SQL Assistant is a web application that allows users to query CSV datasets using plain English.
The system converts natural language questions into optimized SQL queries using an LLM and
displays the results along with visualizations and explanations.

This tool helps users analyze data without writing SQL queries manually.

## 🚀 Features

- Upload any CSV dataset
- Ask questions in plain English
- Automatic SQL query generation
- Execute queries on SQLite database
- Interactive data visualization
- AI-generated explanations for results

## 🛠 Tech Stack

- Python
- Streamlit
- SQLite
- Gemini API (LLM)
- Pandas
- Plotly

## 📂 Project Structure

ai-sql-assistant
│
├── app.py # Streamlit UI
├── database.py # SQLite database handling
├── llm.py # Natural language to SQL generation
├── chart_generator.py # Visualization generation
├── explain_results.py # AI explanation of results
│
├── utils/
│ └── schema_helper.py # Dataset schema extraction
│
├── requirements.txt
├── README.md
└── .gitignore

## 🔄 Workflow

1. Upload CSV dataset
2. Enter question in plain English
3. LLM generates SQL query
4. Query executes on SQLite database
5. Results and charts are displayed
6. AI explains the insights

## 🔮 Future Improvements

- Chat-based interface
- Multiple dataset support
- Automatic SQL error correction
- Dashboard generation

## 👨‍💻 Author

# Shivesh Bajpai

# aisqlassitant

AI-powered web app that converts natural language questions into optimized SQL queries and visualizes results from uploaded CSV datasets.

> > > > > > > 0a702cc84f28aaedbef6e723de04306b782db428
