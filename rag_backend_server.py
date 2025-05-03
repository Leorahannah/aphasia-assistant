from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import numpy as np
from numpy.linalg import norm
from openai import OpenAI

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print("OpenAI client initialized.")

# Load  embeddings and examples
print("Loading precomputed embeddings...")
leora_embeddings = np.load("leora_embeddings.npy")
with open("leora_texts.json", "r", encoding="utf-8") as f:
    leora_data = json.load(f)
print(f"Loaded {len(leora_data)} examples with embeddings.")

# Embed string with OpenAI API
def get_embedding(text):
    res = client.embeddings.create(
        model="text-embedding-ada-002",
        input=[text]
    )
    return np.array(res.data[0].embedding)

# Cosine similarity
def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b) + 1e-10)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    keywords = data.get("keywords", "").strip()
    context = data.get("context", "").strip()

    if not keywords:
        return jsonify({"completions": ["(No keywords provided)"]}), 400

    user_input = f"{context}\n{keywords}".strip()
    try:
        user_embedding = get_embedding(user_input)
        similarities = [cosine_similarity(user_embedding, e) for e in leora_embeddings]
        top_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)[:10]
        top_examples = [leora_data[i] for i in top_indices]
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"completions": ["(Error processing input)"]}), 500

    # Create prompt
    examples_text = "\n".join(f"- {ex}" for ex in top_examples)
    prompt = f"""
You are helping someone with aphasia complete a message. 
They can only type 2–5 keywords at a time. 
You are acting as an AI assistant who helps complete those sentences naturally, in the tone of Leora Klee.

Below is the conversation so far:
{context}

They just typed these keywords:
"{keywords}"

Here are examples of how Leora tends to write:
{examples_text}

Write 3 short sentence suggestions in her tone that could naturally follow this conversation and match those keywords. List each suggestion on its own line.
"""

    # Generate completions
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You complete aphasic messages in Leora's voice."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )

        raw_output = response.choices[0].message.content.strip()
        completions = [line.strip("- ").strip() for line in raw_output.split("\n") if line.strip()]
        return jsonify({"completions": completions[:3]})
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return jsonify({"completions": ["(Error generating completions)"]}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
