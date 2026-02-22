# Aphasia Sentence Completion Assistant

This project is a personalized sentence generation system designed to support individuals with aphasia who struggle to form complete sentences. By combining Retrieval-Augmented Generation (RAG), OpenAI’s API, and a custom vector database built from a user’s past writing, the assistant helps approximate what someone might have meant when they enter just a few keywords. The goal is to bridge gaps in communication while preserving the user's voice and intent.

This project was developed as part of ongoing research into accessible computing and augmentative communication.

---

## ✨ Key Features

- **Keyword-based input** → full, natural-sounding sentence output
- \ **Personal tone & style** through embedded writing samples
- Fast completions powered by OpenAI + ChromaDB
- Web-based frontend for user-friendly interaction
- Built with accessibility and real-world use cases in mind

---

## Project Structure

```
aphasia-assistant/
├── leora-aphasia-chat/              # React frontend (keyword input + output UI)
├── rag_backend_server.py           # Flask backend server
├── precompute_leora_embeddings.py  # Embeds writing samples into Chroma
├── requirements.txt                # Python backend dependencies
├── .gitignore
└── README.md
```

---

## Setup Instructions

### 1. Backend (Flask + OpenAI)

Install dependencies and run the server:

```bash
pip install -r requirements.txt
python rag_backend_server.py
```

Make sure your OpenAI API key is set as an environment variable:

```bash
export OPENAI_API_KEY=your-key-here
```

---

### 2. Frontend (React)

Navigate to the React app and run it:

```bash
cd leora-aphasia-chat
npm install
npm start
```

It’ll run at http://localhost:3000.

---

## Example

**Input keywords:**
```
sick weekend dog
```

**Output:**

> I was feeling really sick this weekend, but I still had to take care of my dog.

This output is generated in the user's tone based on writing samples they've provided (in this case, Leora’s past texts).

---

## How It Works

1. The user enters a few keywords
2. The backend retrieves the most semantically similar past writing samples from the vector DB
3. These samples, along with the keywords and conversation context, are passed to the OpenAI API
4. The model returns a full sentence that aligns with the user's style and intent

---

## Privacy & Personalization

- All completions are generated *only* using the user’s own writing samples (locally stored)
- No writing data is uploaded or included in this public repository
- API keys are kept private using environment variables
- The `.gitignore` ensures local DB files and embeddings aren’t pushed to GitHub

---

## Future Work

- Live editing or correction of completions in real-time
- Integration with mobile keyboard interfaces (iMessage, WhatsApp)
- Collaborations with individuals with aphasia and speech-language pathologists
- Evaluation pipeline for output accuracy vs. intent

---

## 👩‍💻 Created By

Leora Klee  
Computer Science @ McGill University  
With support from Professor Karyn Moffatt and McGill’s Accessible Computing Technologies Research Group
