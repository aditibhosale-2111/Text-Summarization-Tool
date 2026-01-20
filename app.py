# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from model import summarize_text

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/api/summarize", methods=["POST"])
def api_summarize():
    """
    Expected JSON payload:
    {
      "text": "long text to summarize"
    }
    """
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON payload."}), 400

    text = data.get("text", "")

    if not text or len(text.strip()) < 20:
        return jsonify({"error": "Enter at least 20 characters of text."}), 400

    try:
        summary = summarize_text(text)
    except Exception as e:
        return jsonify({"error": "Summarization failed: " + str(e)}), 500

    return jsonify({"summary": summary})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
