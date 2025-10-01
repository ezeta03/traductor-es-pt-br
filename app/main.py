from flask import Flask, request, jsonify
from translator import translate_text

app = Flask(__name__)

@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    translated = translate_text(text)
    return jsonify({"translated_text": translated})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
