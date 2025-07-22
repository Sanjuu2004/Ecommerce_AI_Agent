import sqlite3
from app._gemini_connector import ask_gemini

def run_query(question: str, db_path="database/ecommerce.db") -> list[tuple]:
    """
    Converts a natural language question to SQL using Gemini,
    executes the SQL on the ecommerce.db SQLite database.
    Returns results as a list of tuples.
    """
    try:
        # Step 1: Get SQL from Gemini
        sql_query = ask_gemini(question)
        print(f"Raw SQL from Gemini:\n{sql_query}\n")

        # Step 2: Clean up SQL from markdown formatting
        if not sql_query:
            return [("Error:", "Empty SQL returned from Gemini")]

        # Remove code block if it exists
        if "```" in sql_query:
            parts = sql_query.split("```")
            if len(parts) >= 2:
                sql_query = parts[1].replace("sql", "").strip()
            else:
                return [("Error:", "Unable to parse SQL block")]

        sql_query = sql_query.strip()
        print(f"Cleaned SQL:\n{sql_query}\n")

        if not sql_query:
            return [("Error:", "Final SQL is empty after cleaning")]

        # Step 3: Run SQL on SQLite DB
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        conn.close()

        return results if results else [("Notice:", "Query executed but returned no results.")]

    except Exception as e:
        return [("Error:", str(e))]
