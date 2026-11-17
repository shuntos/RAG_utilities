# RAG Utilities

Code for Retrieval-Augmented Generation (RAG): practical, runnable implementations that use local models.

RAG lets a language model answer questions from your own data. Instead of relying only on what the model learned
during training, it first **retrieves** the most relevant pieces of your documents, **augments** the prompt with
them, and then **generates** an answer from that context. When your data changes, the answers change too, with no
retraining.

## Projects

| Folder | What it is |
|---|---|
| [basic_rag_chatbot](basic_rag_chatbot/) | A RAG chatbot for a fictional fruit shop. It chunks the shop's records, embeds them with `nomic-embed-text`, finds the closest chunks by cosine similarity, and answers with `qwen3:4b-instruct`. Everything runs locally through Ollama. |

Each project has its own README with setup and run instructions.

## Requirements

- [Ollama](https://ollama.com/download) to run the models locally
- Python 3.9+
