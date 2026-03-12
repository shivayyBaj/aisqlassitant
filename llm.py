import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from .env
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

# Load model
model = genai.GenerativeModel("gemini-3-flash-preview")


def generate_sql(question, schema):

    prompt = f"""
You are an expert SQL generator.

Table Name: data_table

Columns:
{schema}

Rules:
- Only generate SQL query
- Use SQLite syntax
- Do not explain

Question:
{question}
"""

    response = model.generate_content(prompt)

    sql = response.text

    # Remove markdown formatting if model returns it
    sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql