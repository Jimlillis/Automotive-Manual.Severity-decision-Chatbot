# Automotive Manual ChatBot

An AI-powered chatbot for answering questions about vehicle manuals using Retrieval-Augmented Generation (RAG). Upload any vehicle manual PDF, ask questions in natural language, and get accurate answers with page references — all running locally with no cloud LLM required.

Built for **Automotive Hackathon 2026**.

---

## How It Works

```
PDF Manual → Text Extraction → Chunking → ChromaDB (vector store)
                                                  ↓
User Question → Semantic Search → Relevant Chunks → Ollama (LLaMA 3) → Answer + Page Sources
```

1. PDFs are extracted page-by-page using PyMuPDF and split into overlapping text chunks
2. Chunks are embedded and stored in a persistent ChromaDB vector database
3. On each question, the most semantically relevant chunks are retrieved via cosine similarity
4. A local LLaMA 3 model (via Ollama) uses those chunks as context to generate a grounded answer
5. All answers include source page references from the original manual

---

## Features

- **Fully local** — no OpenAI or cloud API required; runs on Ollama + LLaMA 3
- **Multi-manual support** — upload and query multiple manuals; filter queries to a specific manual
- **Idempotent ingestion** — re-ingesting the same PDF won't create duplicates
- **Dynamic relevance filtering** — chunks below a similarity threshold are automatically excluded
- **Web UI** — drag-and-drop PDF upload, chat interface, status indicators
- **REST API** — full FastAPI backend for programmatic access

---

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com) installed and running
- LLaMA 3 model pulled:
  ```bash
  ollama pull llama3
  ```

---

## Quick Start

```bash
# 1. Clone the repo
git clone <repo-url>
cd Automotive-Manual-Chatbot/manual-bot

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env         # defaults work out of the box with Ollama

# 5. Start the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open `frontend/index.html` in your browser.

**Windows shortcut:** run `run.bat` — it handles steps 2–5 automatically.

---

## Usage

### Web Interface

1. Open `frontend/index.html`
2. Drag and drop (or click to upload) a vehicle manual PDF
3. Click **Ingest Manuals** to process it into the knowledge base
4. Type your question and press Enter

### REST API

```bash
# Upload a manual
curl -X POST -F "file=@manual.pdf" http://localhost:8000/upload-manual

# Ingest all uploaded manuals
curl -X POST http://localhost:8000/ingest

# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the recommended tire pressure?"}'

# Ask about a specific manual
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I reset the service light?", "manual_name": "bmw_x5_2025.pdf"}'

# Search without generating an answer
curl "http://localhost:8000/retrieve?query=oil+change+interval"

# List available manuals
curl http://localhost:8000/manuals

# Clear the vector database
curl -X DELETE http://localhost:8000/clear-database
```

---

## Configuration

Edit `.env` to tune behaviour:

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_MODEL` | `llama3` | Model to use via Ollama |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server URL |
| `CHUNK_SIZE` | `1024` | Characters per text chunk |
| `CHUNK_OVERLAP` | `100` | Overlap between adjacent chunks |
| `TOP_K_CHUNKS` | `8` | Max chunks fetched before relevance filtering |
| `APP_PORT` | `8000` | Backend server port |

---

## Project Structure

```
manual-bot/
├── app/
│   ├── main.py        # FastAPI app and API endpoints
│   ├── rag.py         # RAGSystem + VectorDatabase (ChromaDB)
│   ├── ingest.py      # PDF extraction and chunking (PyMuPDF)
│   ├── prompts.py     # LLM system prompt and templates
│   ├── config.py      # Settings loaded from .env
│   └── utils.py       # Text cleaning and formatting helpers
├── frontend/
│   └── index.html     # Single-page web UI
├── data/
│   ├── manuals/       # Drop PDF files here
│   └── chroma_db/     # Persisted vector database (auto-created)
├── tests/
│   └── test_app.py
├── requirements.txt
├── requirements-dev.txt
└── .env.example
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | [Ollama](https://ollama.com) + LLaMA 3 (local) |
| Vector DB | [ChromaDB](https://www.trychroma.com/) |
| PDF Parsing | [PyMuPDF](https://pymupdf.readthedocs.io/) |
| Backend | [FastAPI](https://fastapi.tiangolo.com/) + Uvicorn |
| Frontend | Vanilla HTML/CSS/JS |

---

## License

This project was built for the Automotive Manual Chatbot Hackathon 2026.
