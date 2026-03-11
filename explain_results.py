import google.generativeai as genai

def explain(question, result):

    prompt = f"""
Explain the result of this query in simple English.

Question:
{question}

Result:
{result.head().to_string()}
"""

    model = genai.GenerativeModel("gemini-3-flash-preview")
    response = model.generate_content(prompt)

    return response.text