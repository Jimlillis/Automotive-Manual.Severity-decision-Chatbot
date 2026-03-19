import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # API Configuration
    APP_NAME: str = "Automotive Manual ChatBot"
    APP_VERSION: str = "1.0.0"
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", 8000))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
    
    # Chroma Vector Database
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "./data/chroma_db")
    COLLECTION_NAME: str = "automotive_manuals"
    
    # Paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    MANUALS_DIR: Path = DATA_DIR / "manuals"
    
    # Model hyperparameters
    CHUNK_SIZE: int = 1024
    CHUNK_OVERLAP: int = 100
    TOP_K_CHUNKS: int = 5
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 1000

settings = Settings()
