@echo off
REM Run script for Automotive Manual ChatBot (Windows)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo ^^!^! Please edit .env and add your OPENAI_API_KEY
    echo.
)

REM Create data directories
echo Creating data directories...
if not exist "data\manuals" mkdir data\manuals
if not exist "data\chroma_db" mkdir data\chroma_db

REM Start the application
echo.
echo Starting Automotive Manual ChatBot...
echo ^~ Backend will run at: http://localhost:8000
echo ^~ Frontend: Open frontend/index.html in your browser
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
