import google.generativeai as genai

genai.configure(api_key="AIzaSyDIcKecD6s-hfW1cv5r2FmmzhmCDwyleMw")

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

    sql = sql.replace("```sql", "").replace("```", "")

    return sql