#!/bin/bash
# Run script for Automotive Manual ChatBot

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY"
fi

# Create data directories
echo "Creating data directories..."
mkdir -p data/manuals
mkdir -p data/chroma_db

# Start the application
echo "Starting Automotive Manual ChatBot..."
echo "🚗 Backend will run at: http://localhost:8000"
echo "📄 Frontend: Open frontend/index.html in your browser"
echo ""
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
