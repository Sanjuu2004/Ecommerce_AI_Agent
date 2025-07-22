# app/_gemini_connector.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env and configure Gemini API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise EnvironmentError("❌ Gemini API key not found in environment variables!")

genai.configure(api_key=API_KEY)

# Define the model (Lite for speed; switch to pro if needed)
model = genai.GenerativeModel(model_name="models/gemini-2.5-flash-lite")

def ask_gemini(question: str) -> str:
    """
    Converts an English question into a valid SQLite SQL query using Gemini.
    Returns plain SQL as a string.
    """
    prompt = f"""
You are a helpful assistant that converts English questions to SQLite SQL queries.
Only return the SQL query — no explanations, no code formatting like ```sql.
The database has the following tables and columns:

- eligibility(eligibility_datetime_utc, item_id, eligibility, message)
- ad_sales_metrics(date, item_id, ad_sales, impressions, ad_spend, clicks, units_sold)
- total_sales_metrics(date, item_id, total_sales, total_units_ordered)

Join tables using item_id when necessary.
Avoid using any markdown formatting.
Return only valid, executable SQL.

Question: {question}
SQL:"""

    try:
        response = model.generate_content(prompt)
        sql = response.text.strip()

        # Basic sanitization
        if not sql.lower().startswith("select"):
            raise ValueError("Gemini response did not contain a valid SQL SELECT statement.")

        return sql

    except Exception as e:
        return f"SELECT 'Error: {str(e)}' AS error_message;"
