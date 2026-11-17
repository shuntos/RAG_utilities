import csv
import requests
import numpy as np
from pathlib import Path

OLLAMA_END_POINT = "http://localhost:11434"

EMBEDDING_MODEL = "nomic-embed-text"
LANG_MODEL = "qwen3:4b-instruct"

# Big day-by-day history files: thousands of rows, too slow to embed for a demo
SKIP_FILES = {
    "README.txt",
    "sales_2025.csv",
    "waste_2025.csv",
    "deliveries_2025.csv",
    "staff_shifts_2025.csv",
    "expenses_2025.csv",
    "daily_summary_2025.csv",
}


def generate_embedding(text):
    r = requests.post(
        f"{OLLAMA_END_POINT}/api/embed",
        json={"model": EMBEDDING_MODEL, "input": text},
    )
    return np.array(r.json()["embeddings"])


def lang_model_req(prompt):
    r = requests.post(
        f"{OLLAMA_END_POINT}/api/generate",
        json={"model": LANG_MODEL, "prompt": prompt, "stream": False},
    )
    return r.json()["response"]


def chunk_documents(folder):
    chunks = []

    for file in Path(folder).iterdir():
        if file.name in SKIP_FILES:
            continue

        # Text files: one chunk per paragraph (split on empty lines)
        if file.suffix == ".txt":
            for paragraph in file.read_text(encoding="utf-8").split("\n\n"):
                if paragraph.strip():
                    chunks.append(f"[{file.name}] {paragraph.strip()}")

        # Inventory: keep only the latest day, written as a simple sentence
        elif file.name == "inventory_daily_2025.csv":
            with open(file, encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            last_date = rows[-1]["date"]
            for row in rows:
                if row["date"] == last_date:
                    chunks.append(
                        f"[{file.name}] We have {row['closing_units']} {row['fruit']} in stock."
                    )

        # Other CSV files: one chunk per row, written as "column: value"
        elif file.suffix == ".csv":
            with open(file, encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    text = ", ".join(f"{key}: {value}" for key, value in row.items())
                    chunks.append(f"[{file.name}] {text}")

    return chunks


def retrieve_context(user_input, k=3):
    query_embedding = generate_embedding(user_input)[0]

    # cosine similarity between the question and every chunk
    scores = list_of_embedding @ query_embedding / (
        np.linalg.norm(list_of_embedding, axis=1) * np.linalg.norm(query_embedding)
    )

    best = np.argsort(scores)[::-1][:k]
    top_contexts = [chunks_list[i] for i in best]

    return top_contexts


chunks_list = chunk_documents("shop_records")
print(f"Created {len(chunks_list)} chunks")

list_of_embedding = generate_embedding(chunks_list)
print(f"Created embeddings: {list_of_embedding.shape}\n")


while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ("exit", "quit"):
        break
    if not user_input:
        continue

    top_context = retrieve_context(user_input)
    context = "\n".join(top_context)

    prompt = f"""You are a helpful assistant for a fruit shop.
Answer the question using ONLY the context below. Keep the answer short.
If the answer is not in the context, reply exactly: I don't know.

Context:
{context}

Question: {user_input}
Answer:"""

    output = lang_model_req(prompt)

    print(f"\n[Retrieved context]\n{context}\n")
    print(f"AI: {output}\n")
