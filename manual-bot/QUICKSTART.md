# Quick Start Guide

Get the Automotive Manual ChatBot running in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- OpenAI API key (get one at https://platform.openai.com/api-keys)
- A vehicle manual PDF (optional, for testing)

## Installation (Windows)

### Step 1: Navigate to project directory
```powershell
cd "path\to\manual-bot"
```

### Step 2: Run startup script
```powershell
.\run.bat
```

This will:
- Create a virtual environment
- Install all dependencies
- Setup configuration files
- Start the backend server

### Step 3: Configure API Key
After the script completes:
1. Open the newly created `.env` file
2. Replace `your_openai_api_key_here` with your actual OpenAI API key
3. Save the file

### Step 4: Start Backend (if not already running)
```powershell
.\run.bat
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 5: Open Frontend
Open `frontend/index.html` in your browser, or navigate to:
```
http://localhost:3000
```

Or run a local server:
```powershell
python -m http.server 3000 --directory frontend
```

## Usage

### 1. Upload a Manual
- Click "📄 Upload Manual" area
- Drag and drop or click to select a PDF
- File should be a vehicle manual in PDF format

### 2. Ingest Manuals
- After uploading, click "Ingest Manuals"
- Wait for the status badge to show "System Ready"
- This processes the PDF and indexes it

### 3. Ask Questions
- Type your question in the input field
- Examples:
  - "How do I change the oil?"
  - "What is the recommended tire pressure?"
  - "How do I reset the maintenance light?"
- Click "Send" or press Enter

### 4. View Answers
- The chatbot will retrieve relevant manual sections
- Generate an answer using AI
- Show source page references
- Display tokens used and chunks retrieved

## Installation (Mac/Linux)

### Step 1: Navigate to project directory
```bash
cd path/to/manual-bot
```

### Step 2: Run startup script
```bash
chmod +x run.sh
./run.sh
```

### Step 3-5: Same as Windows steps above

## Troubleshooting

### "OPENAI_API_KEY is not set"
✅ **Solution**: 
1. Open `.env` file
2. Add your OpenAI API key
3. Restart the server

### "No documents found" or "No relevant manual sections"
✅ **Solution**:
1. Check that you've uploaded a PDF
2. Confirm the file is a readable PDF
3. Click "Ingest Manuals" button
4. Wait for status to show "Ready"
5. Try your question again

### Backend won't start
✅ **Solution**:
```bash
# Kill any existing process on port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID [PID] /F

# Mac/Linux:
lsof -i :8000
kill -9 [PID]

# Then restart
./run.bat  # or ./run.sh
```

### Slow responses
✅ **Solution**:
- Reduce TOP_K_CHUNKS in `.env` (from 5 to 3)
- Use faster model: `OPENAI_MODEL=gpt-3.5-turbo`
- Ensure manual PDF is not too large

### Frontend doesn't load
✅ **Solution**:
- Ensure backend is running (check port 8000)
- Open browser console (F12) to see errors
- Try opening directly: `file:///path/to/frontend/index.html`

## Project Structure

```
manual-bot/
├── run.bat              ← Start here (Windows)
├── run.sh               ← Start here (Mac/Linux)
├── .env                 ← Your API key goes here
├── requirements.txt     ← Python dependencies
├── app/                 ← Backend code
│   ├── main.py         ← FastAPI server
│   ├── rag.py          ← AI logic
│   ├── ingest.py       ← PDF processing
│   └── ...
├── frontend/            ← Web interface
│   └── index.html      ← Open this in browser
└── data/
    ├── manuals/        ← Upload PDFs here
    └── chroma_db/      ← Database (auto-created)
```

## Common Questions

### Q: Can I use multiple PDFs?
**A**: Yes! Upload as many as you want. They'll all be indexed.

### Q: Do you store my documents?
**A**: Documents are stored locally in `data/chroma_db/`. Not sent anywhere unless you use the API.

### Q: Can I change the AI model?
**A**: Yes! Edit `.env`:
```env
OPENAI_MODEL=gpt-3.5-turbo  # Faster, cheaper
OPENAI_MODEL=gpt-4          # More accurate
OPENAI_MODEL=gpt-4-turbo    # Balanced
```

### Q: What if I run out of API quota?
**A**: You'll get an error. Check your OpenAI account at platform.openai.com

### Q: Can I deploy this?
**A**: Yes! See [DEPLOYMENT.md](DEPLOYMENT.md) for options (Docker, Heroku, AWS, etc.)

## API Usage

For programmatic access, use the REST API:

```bash
# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I change the oil?"}'

# Get configuration
curl http://localhost:8000/config
```

See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for full reference.

## Next Steps

1. **Read**: Check out [README.md](README.md) for comprehensive documentation
2. **Deploy**: Explore [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
3. **API**: Learn the [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for programmatic usage
4. **Customize**: Adjust prompts in `app/prompts.py`
5. **Test**: Run `pytest` if you modify code

## Tips & Tricks

### Better Answers
- Use specific questions: ❌ "Tell me about the car" → ✅ "How do I reset the engine light?"
- Upload the official manual for your vehicle model
- Ask follow-up questions to clarify

### Performance
- Keep PDFs under 500 pages for faster ingestion
- Use `gpt-3.5-turbo` for budget/speed
- Clear database before ingesting new manuals

### Development
```bash
# Run with debug mode
set DEBUG=true  # Windows
export DEBUG=true  # Mac/Linux
./run.bat  # or ./run.sh

# Run tests
pytest

# Code formatting
black app/
```

## Support

- Check [README.md](README.md) - Comprehensive guide
- Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API reference
- Check [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- Review logs in terminal for error messages

---

**Ready to start?** Run `./run.bat` or `./run.sh` now! 🚗
