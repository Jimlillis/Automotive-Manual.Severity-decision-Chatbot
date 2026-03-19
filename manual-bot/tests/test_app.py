"""
Test suite for Automotive Manual ChatBot
"""

import pytest
from pathlib import Path
from app.ingest import PDFProcessor
from app.utils import (
    clean_text, format_context, format_sources,
    validate_pdf_path, truncate_text, ensure_directory_exists
)


class TestPDFProcessor:
    """Test PDF processing functionality"""
    
    def test_pdf_processor_initialization(self):
        """Test PDFProcessor initialization"""
        processor = PDFProcessor(chunk_size=1024, chunk_overlap=100)
        assert processor.chunk_size == 1024
        assert processor.chunk_overlap == 100
    
    def test_create_chunks(self):
        """Test text chunking"""
        processor = PDFProcessor(chunk_size=100, chunk_overlap=20)
        text = "This is a test. " * 20
        chunks = processor.create_chunks(text, page_number=1)
        
        assert len(chunks) > 0
        assert all(chunk['page'] == 1 for chunk in chunks)
        assert all('content' in chunk for chunk in chunks)


class TestUtilities:
    """Test utility functions"""
    
    def test_clean_text(self):
        """Test text cleaning"""
        dirty_text = "This   is\n\n  a   test"
        clean = clean_text(dirty_text)
        assert "   " not in clean
        assert "\n" not in clean
    
    def test_format_context(self):
        """Test context formatting"""
        chunks = [
            {"content": "Text 1", "page": 1},
            {"content": "Text 2", "page": 2}
        ]
        context = format_context(chunks)
        assert "Text 1" in context
        assert "Text 2" in context
        assert "[Page 1]" in context
    
    def test_format_sources(self):
        """Test source formatting"""
        chunks = [
            {"page": 1},
            {"page": 5},
            {"page": 1}
        ]
        sources = format_sources(chunks)
        assert "Page 1" in sources
        assert "Page 5" in sources
    
    def test_truncate_text(self):
        """Test text truncation"""
        text = "a" * 1000
        truncated = truncate_text(text, max_length=100)
        assert len(truncated) <= 103  # 100 + "..."
        assert truncated.endswith("...")
    
    def test_ensure_directory_exists(self):
        """Test directory creation"""
        test_dir = Path("test_dir_temp")
        ensure_directory_exists(str(test_dir))
        assert test_dir.exists()
        # Cleanup
        test_dir.rmdir()


class TestRAGSystem:
    """Test RAG system (requires API key)"""
    
    @pytest.mark.skip(reason="Requires OpenAI API key")
    def test_rag_initialization(self):
        """Test RAG system initialization"""
        from app.rag import RAGSystem
        rag = RAGSystem()
        assert rag.model is not None
        assert rag.vector_db is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
