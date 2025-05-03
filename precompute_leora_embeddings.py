
import json
import numpy as np
import os
from openai import OpenAI
from tqdm import tqdm

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load all examples
with open("leora_training_data.jsonl", "r", encoding="utf-8") as f:
    leora_data = [json.loads(line)["output"] for line in f if line.strip()][:500]

print(f"Loaded {len(leora_data)} examples.")

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=[text]
    )
    return response.data[0].embedding

# Compute and save embeddings
embeddings = []
for sentence in tqdm(leora_data, desc="Embedding sentences"):
    try:
        emb = get_embedding(sentence)
        embeddings.append(emb)
    except Exception as e:
        print(f"Failed to embed: {sentence[:50]}... — {e}")
        embeddings.append([0.0] * 1536)  # fallback zero vector

# Save both sentences and embeddings
np.save("leora_embeddings.npy", np.array(embeddings))
with open("leora_texts.json", "w", encoding="utf-8") as f:
    json.dump(leora_data, f, ensure_ascii=False)

print(" Saved leora_embeddings.npy and leora_texts.json")
