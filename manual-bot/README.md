# Automotive Manual ChatBot - RAG System

An AI-powered web application for answering vehicle manual questions using Retrieval-Augmented Generation (RAG).

## Features

✅ **PDF Processing**: Accepts vehicle manuals in PDF format
✅ **Semantic Search**: Extracts and chunks manual text with intelligent retrieval
✅ **Vector Database**: Stores embeddings in Chroma vector database
✅ **LLM Integration**: Uses OpenAI GPT-4 for intelligent question answering
✅ **Source Attribution**: Returns page references for all answers
✅ **Web Interface**: Clean, modern UI for interactions
✅ **REST API**: FastAPI backend with comprehensive endpoints
✅ **File Management**: Upload, ingest, and manage multiple manuals

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Frontend (HTML/JS)                 │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────v────────────────────────────────┐
│            FastAPI Backend (main.py)                │
│  - /ask (question answering)                        │
│  - /upload-manual (file upload)                     │
│  - /ingest (process PDFs)                           │
│  - /retrieve (document search)                      │
└────┬──────────────┬──────────────┬──────────────────┘
     │              │              │
     v              v              v
┌────────────┐ ┌─────────────┐ ┌──────────────┐
│   RAG      │ │   Vector    │ │   OpenAI     │
│  System    │ │  Database   │ │     API      │
│  (rag.py)  │ │  (Chroma)   │ │   (GPT-4)    │
└────┬───────┘ └─────────────┘ └──────────────┘
     │
 ┌───v────────────────┐
 │  PDF Processor     │
 │  (ingest.py)       │
 └────────────────────┘
```

## Installation

### Prerequisites
- Python 3.8+
- OpenAI API key
- pip or conda

### Setup Steps

1. **Clone/Navigate to the project**:
   ```bash
   cd manual-bot
   ```

2. **Create virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   # Copy example file
   cp .env.example .env
   
   # Edit .env and add your OpenAI API key
   # OPENAI_API_KEY=sk-your-key-here
   ```

5. **Create data directories**:
   ```bash
   mkdir -p data/manuals
   mkdir -p data/chroma_db
   ```

## Usage

### Option 1: Using the Web Interface (Recommended)

1. **Start the backend server**:
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Open the frontend**:
   - Open `frontend/index.html` in a web browser
   - Or navigate to `http://localhost:8000`

3. **Use the application**:
   - Upload vehicle manual PDFs
   - Click "Ingest Manuals" to process them
   - Ask questions about the manuals

### Option 2: Using the REST API

```bash
# Health check
curl http://localhost:8000/health

# Upload a manual
curl -X POST -F "file=@manual.pdf" http://localhost:8000/upload-manual

# Ingest all manuals
curl -X POST http://localhost:8000/ingest

# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I change the oil?"}'

# Search documents
curl "http://localhost:8000/retrieve?query=tire%20pressure"

# Clear database
curl -X DELETE http://localhost:8000/clear-database
```

## API Endpoints

### Health & Status
- `GET /` - Root endpoint
- `GET /health` - System health check
- `GET /config` - Get system configuration

### Question Answering
- `POST /ask` - Ask a question about manuals
  - Request: `{"question": "...", "top_k": 5}`
  - Response: `{"answer": "...", "sources": "...", "retrieved_chunks": 5, "tokens_used": 250}`

- `GET /retrieve` - Search documents without generating answer
  - Query: `?query=...&top_k=5`

### Manual Management
- `POST /upload-manual` - Upload a PDF manual
- `POST /ingest` - Ingest all PDFs in manuals directory
- `DELETE /clear-database` - Clear the vector database

## Configuration

Edit `.env` file to customize:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4

# Server Configuration
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=False

# RAG Parameters
CHUNK_SIZE=1024
CHUNK_OVERLAP=100
TOP_K_CHUNKS=5
TEMPERATURE=0.7
MAX_TOKENS=1000
```

## Project Structure

```
manual-bot/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── rag.py           # RAG system implementation
│   ├── ingest.py        # PDF processing
│   ├── prompts.py       # LLM prompts
│   ├── utils.py         # Helper functions
│   └── config.py        # Configuration management
├── frontend/
│   └── index.html       # Web interface
├── data/
│   ├── manuals/         # Store PDF files here
│   └── chroma_db/       # Vector database
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

## Key Components

### RAG System (rag.py)
- `VectorDatabase` - Manages Chroma vector database
- `RAGSystem` - Main RAG pipeline orchestrator
- Methods: `ingest_manuals()`, `retrieve()`, `generate_answer()`, `answer_question()`

### PDF Processor (ingest.py)
- `PDFProcessor` - Handles PDF extraction and chunking
- Methods: `extract_text_from_pdf()`, `create_chunks()`, `process_pdf()`

### FastAPI Backend (main.py)
- Async request handling
- CORS enabled for frontend integration
- Comprehensive error handling
- Request/response validation with Pydantic

## Performance Tips

1. **Chunk Size**: Larger chunks (2048) for better context, smaller (512) for faster retrieval
2. **Top K**: Balance between relevance (5-10) and response time
3. **Temperature**: Lower (0.3-0.5) for factual answers, higher (0.7-0.9) for creative responses
4. **Database**: Persist vector database between sessions for faster startup

## Troubleshooting

### "OPENAI_API_KEY is not set"
- Make sure `.env` file exists with valid API key
- Check that `export OPENAI_API_KEY=...` is set (if not using .env)

### "No documents found"
- Verify PDFs are in `data/manuals/` directory
- Click "Ingest Manuals" button to process them
- Check browser console for errors

### Slow responses
- Reduce `TOP_K_CHUNKS` in `.env`
- Use a faster OpenAI model like `gpt-3.5-turbo`
- Ensure vector database is on fast storage

### CORS errors
- Backend has CORS enabled for all origins by default
- Modify CORS settings in `main.py` if needed

## Future Enhancements

- [ ] Support for multiple manual formats (PDF, Word, etc.)
- [ ] Multi-language support
- [ ] User authentication and sessions
- [ ] Chat history persistence
- [ ] Advanced embedding models (Sentence Transformers)
- [ ] Admin panel for database management
- [ ] Analytics and usage tracking
- [ ] Docker containerization

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is part of the Automotive Manual Chatbot Hackathon 2026.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the API documentation
3. Check backend logs in terminal
4. Open an issue in the repository

---

**Created**: March 2026
**Version**: 1.0.0