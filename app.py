from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a savage roasting AI for Telegram groups.
Reply to messages with harsh, funny Hinglish roasts.
No religion, caste, race, gender, sexuality.
Short, brutal, sarcastic.
"""

@app.route("/")
def home():
    return "🔥 AI Roast API Running 🔥"

@app.route("/roast", methods=["POST"])
def roast():
    data = request.json
    message = data.get("message", "")

    prompt = f"Roast this group message:\n{message}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=1.2,
        max_tokens=60
    )

    return jsonify({
        "roast": response.choices[0].message.content.strip()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))