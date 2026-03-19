"""
Automotive Manual ChatBot Application
"""

from app.rag import RAGSystem, VectorDatabase
from app.ingest import PDFProcessor, ingest_manuals
from app.config import settings

__version__ = "1.0.0"
__all__ = ["RAGSystem", "VectorDatabase", "PDFProcessor", "ingest_manuals", "settings"]
