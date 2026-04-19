from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from groq import Groq

app = Flask(__name__)

load_dotenv()
api_key = os.getenv("groq_api_key")

# Initialize Groq client
client = Groq(api_key=api_key)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        question = request.form.get("question")
        mode = request.form.get("mode")

        if not question:
            return jsonify({"error": "No input provided"}), 400

        # 🎯 Dynamic system prompts
        system_prompts = {
            "chat": "You are a helpful personal assistant.",
            "summarize": "Summarize the given text in 2-3 concise sentences.",
            "code": "Explain the following code in simple terms step by step.",
            "rewrite": "Rewrite the following text in a clearer and more professional way."
        }

        system_prompt = system_prompts.get(mode, "You are a helpful assistant.")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=512
        )

        answer = response.choices[0].message.content.strip()

        return jsonify({"response": answer}), 200

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        email_text = request.form.get("email")

        if not email_text:
            return jsonify({"error": "No email provided"}), 400

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Act like an expert email assistant"},
                {"role": "user", "content": f"Summarize the following email in 2-3 sentences:\n{email_text}"}
            ],
            temperature=0.3,
            max_tokens=512
        )

        summary = response.choices[0].message.content.strip()

        return jsonify({"response": summary}), 200

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run()