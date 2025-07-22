from flask import Flask, request, jsonify
from app.query_engine import run_query
import traceback

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask_question():
    try:
        data = request.json
        question = data.get("question")

        if not question:
            return jsonify({"error": "No question provided"}), 400

        # Run the Gemini → SQL → SQLite pipeline
        results = run_query(question)

        # Check if error occurred during SQL execution
        if isinstance(results, dict) and "error" in results:
            return jsonify({"error": results["error"]}), 500

        return jsonify({
            "question": question,
            "results": results
        })

    except Exception as e:
        print("❌ Exception in /ask endpoint:", e)
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
