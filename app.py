from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY missing")
    return OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
You are a savage roasting AI for Telegram groups.
Reply with harsh, funny Hinglish roasts.
No religion, caste, race, gender, sexuality.
Short, brutal, sarcastic.
"""

@app.route("/")
def home():
    return "🔥 AI Roast API Running 🔥"

@app.route("/roast", methods=["POST"])
def roast():
    data = request.json or {}
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "message required"}), 400

    try:
        client = get_client()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Roast this message:\n{message}"}
            ],
            temperature=1.2,
            max_tokens=60
        )

        return jsonify({
            "roast": response.choices[0].message.content.strip()
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
