# Basic RAG Chatbot (Fruit Shop)

A small Retrieval-Augmented Generation (RAG) chatbot that runs entirely on your own machine.
It answers questions about a fictional fruit shop using the shop's own records, not just what the
language model learned during training.

No internet connection or API key is needed once the models are downloaded. Everything runs locally
through [Ollama](https://ollama.com).

## How it works

```
shop_records/  ──►  chunk  ──►  embed (nomic-embed-text)  ──►  vectors in memory
                                                                     │
your question  ──►  embed  ──►  cosine similarity  ──►  top 3 chunks ┘
                                                          │
                              prompt = context + question ▼
                                            qwen3:4b-instruct  ──►  answer
```

1. **Chunking**: the files in `shop_records/` are split into small pieces of text:
   - `.txt` files (handbook, FAQ): one chunk per paragraph.
   - `inventory_daily_2025.csv`: only the latest day, written as a sentence ("We have 42 Mangoes in stock.").
   - other `.csv` files: one chunk per row, written as `column: value` pairs.
   - The large day-by-day history files (sales, waste, deliveries, shifts, expenses, daily summary) are skipped
     so the demo starts quickly. See `SKIP_FILES` in `rag_server.py`.
2. **Embedding**: every chunk is turned into a vector by `nomic-embed-text`.
3. **Retrieval**: your question is embedded too, and the 3 chunks with the highest cosine similarity are picked.
4. **Augmentation**: those chunks are put into the prompt as context.
5. **Generation**: `qwen3:4b-instruct` answers using only that context, and replies "I don't know" if the
   answer isn't there.

## Requirements

- [Ollama](https://ollama.com/download) (Windows, macOS or Linux)
- Python 3.9+
- About 3 GB of disk space for the two models. A regular laptop is enough; a GPU makes answers faster.

## Setup

1. Install Ollama from <https://ollama.com/download> and make sure it is running.

2. Download the two models:

   ```bash
   ollama pull nomic-embed-text
   ollama pull qwen3:4b-instruct
   ```

3. Install the Python packages:

   ```bash
   python -m pip install requests numpy
   ```

4. Check that both models are installed:

   ```bash
   ollama list
   ```

   Optional: chat with the language model directly to make sure it works (type `/bye` to exit):

   ```bash
   ollama run qwen3:4b-instruct
   ```

## Run

Run it from this folder, because the script reads `shop_records/` from the current directory:

```bash
cd basic_rag_chatbot
python rag_server.py
```

It builds the chunks and embeddings first, then waits for your questions:

```
Created N chunks
Created embeddings: (N, 768)

You: Where do your mangoes come from?

[Retrieved context]
[products.csv] product_id: MAN, fruit: Mangoes, origin: India, ...
...

AI: Our mangoes come from India.
```

Type `exit` or `quit` to stop.

### Questions to try

- Where do your mangoes come from?
- How many bananas do you have in stock?
- What are your opening hours?
- Can I get a refund on fruit?
- Which is sweeter, apples or bananas?
- Who supplies the strawberries?

## Project structure

```
basic_rag_chatbot/
├── rag_server.py        # chunking, embeddings, retrieval and the chat loop
└── shop_records/        # synthetic fruit shop dataset (see shop_records/README.txt)
    ├── products.csv, nutrition.csv, suppliers.csv, staff.csv
    ├── inventory_daily_2025.csv
    ├── shop_handbook.txt, customer_faq.txt
    ├── rag_chunks.jsonl  # pre-made chunks (not used by rag_server.py)
    └── *_2025.csv        # large daily history files (skipped by default)
```

## Configuration

At the top of `rag_server.py`:

| Setting | Default | Meaning |
|---|---|---|
| `OLLAMA_END_POINT` | `http://localhost:11434` | Where Ollama is running |
| `EMBEDDING_MODEL` | `nomic-embed-text` | Model that turns text into vectors |
| `LANG_MODEL` | `qwen3:4b-instruct` | Model that writes the answer |
| `SKIP_FILES` | big history files | Files left out of chunking |

`retrieve_context(user_input, k=3)` controls how many chunks go into the prompt.

To use another Ollama model, `ollama pull` it and change `LANG_MODEL`.

## Troubleshooting

- **`ConnectionError` / connection refused**: Ollama isn't running. Start the Ollama app, or run `ollama serve`.
- **`KeyError: 'embeddings'` or `'response'`**: the model isn't downloaded. Run the `ollama pull` commands again
  and check `ollama list`.
- **`FileNotFoundError: shop_records`**: run the script from inside the `basic_rag_chatbot` folder.
- **Slow start**: every chunk is embedded at startup. Keep the large history files in `SKIP_FILES`.

## Limits

- Embeddings are kept in memory and rebuilt on every start. A real app would store them in a vector database.
- Similarity search is good for finding text by meaning, but weak for exact numbers and arithmetic
  (totals, averages over a year). For those, query the CSV files directly (pandas or SQL) and add the result
  to the prompt.
- Inventory is the last day in the dataset (2025-12-31), not live stock.

## Data

`shop_records/` is an entirely synthetic dataset made for this tutorial. It is not real business or health data.
