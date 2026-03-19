"""
Utility functions for the chatbot application
"""

import logging
from typing import List, Dict, Any
import re
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clean_text(text: str) -> str:
    """
    Clean text by removing extra whitespace and special characters
    
    Args:
        text: Raw text to clean
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep punctuation
    text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    return text.strip()


def format_context(chunks: List[dict]) -> str:
    """
    Format retrieved chunks into readable context
    
    Args:
        chunks: List of chunk dictionaries
        
    Returns:
        Formatted context string
    """
    formatted = []
    
    for chunk in chunks:
        page = chunk.get("page", "Unknown")
        content = chunk.get("content", "")
        metadata = f"[Page {page}]"
        formatted.append(f"{metadata}\n{content}")
    
    return "\n\n---\n\n".join(formatted)


def format_sources(chunks: List[dict]) -> str:
    """
    Format source information from chunks
    
    Args:
        chunks: List of chunk dictionaries
        
    Returns:
        Formatted sources string
    """
    sources = set()
    
    for chunk in chunks:
        page = chunk.get("page")
        if page:
            sources.add(f"Page {page}")
    
    if not sources:
        return "Manual references available"
    
    return "Sources: " + ", ".join(sorted(sources))


def validate_pdf_path(pdf_path: str) -> bool:
    """
    Validate if PDF file exists and is readable
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        True if valid PDF path
    """
    path = Path(pdf_path)
    return path.exists() and path.suffix.lower() == ".pdf" and path.is_file()


def get_pdf_files(directory: str) -> List[str]:
    """
    Get all PDF files in a directory
    
    Args:
        directory: Path to directory
        
    Returns:
        List of PDF file paths
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        logger.warning(f"Directory {directory} does not exist")
        return []
    
    pdf_files = list(dir_path.glob("*.pdf"))
    return [str(f) for f in pdf_files]


def truncate_text(text: str, max_length: int = 500) -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."


class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, max_calls: int = 100, time_window: int = 60):
        """
        Initialize rate limiter
        
        Args:
            max_calls: Maximum number of calls
            time_window: Time window in seconds
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
    
    def is_allowed(self, timestamp: float) -> bool:
        """
        Check if a call is allowed
        
        Args:
            timestamp: Current timestamp
            
        Returns:
            True if call is allowed
        """
        # Remove old calls outside the time window
        self.calls = [t for t in self.calls if timestamp - t < self.time_window]
        
        if len(self.calls) < self.max_calls:
            self.calls.append(timestamp)
            return True
        
        return False


def ensure_directory_exists(directory: str) -> None:
    """
    Ensure a directory exists, create if it doesn't
    
    Args:
        directory: Path to directory
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Ensured directory exists: {directory}")
