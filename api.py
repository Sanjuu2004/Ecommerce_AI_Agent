from flask import Flask, request, jsonify
from app.query_engine import run_query

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.json
    question = data.get("question")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        results = run_query(question)
        return jsonify({
            "question": question,
            "results": results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
