"""
PDF ingestion and processing module for vehicle manuals
"""

import fitz  # PyMuPDF
import os
from pathlib import Path
from typing import List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFProcessor:
    """Process PDF files and extract text chunks"""
    
    def __init__(self, chunk_size: int = 1024, chunk_overlap: int = 100):
        """
        Initialize PDF processor
        
        Args:
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks for context preservation
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def extract_text_from_pdf(self, pdf_path: str) -> List[Tuple[str, int]]:
        """
        Extract text from PDF with page numbers
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of (text, page_number) tuples
        """
        try:
            pdf_document = fitz.open(pdf_path)
            pages_content = []
            
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                text = page.get_text()
                pages_content.append((text, page_num + 1))
            
            pdf_document.close()
            logger.info(f"Extracted text from {len(pages_content)} pages from {pdf_path}")
            return pages_content
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF {pdf_path}: {str(e)}")
            raise
    
    def create_chunks(self, text: str, page_number: int) -> List[dict]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Text to chunk
            page_number: Page number reference
            
        Returns:
            List of chunk dictionaries with metadata
        """
        chunks = []
        
        # Clean text
        text = text.strip()
        if not text:
            return chunks
        
        # Create overlapping chunks
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunk = text[i:i + self.chunk_size]
            
            if len(chunk.strip()) > 50:  # Ignore very small chunks
                chunks.append({
                    "content": chunk,
                    "page": page_number,
                    "start_idx": i,
                    "end_idx": i + len(chunk)
                })
        
        return chunks
    
    def process_pdf(self, pdf_path: str) -> List[dict]:
        """
        Process entire PDF and return chunked content with metadata
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of processed chunks with metadata
        """
        pages_content = self.extract_text_from_pdf(pdf_path)
        all_chunks = []
        
        for text, page_num in pages_content:
            chunks = self.create_chunks(text, page_num)
            all_chunks.extend(chunks)
        
        logger.info(f"Created {len(all_chunks)} chunks from {pdf_path}")
        return all_chunks
    
    def process_directory(self, directory_path: str) -> dict:
        """
        Process all PDF files in a directory
        
        Args:
            directory_path: Path to directory containing PDFs
            
        Returns:
            Dictionary mapping filename to chunks
        """
        all_documents = {}
        directory = Path(directory_path)
        
        if not directory.exists():
            logger.warning(f"Directory {directory_path} does not exist")
            return all_documents
        
        pdf_files = list(directory.glob("*.pdf"))
        logger.info(f"Found {len(pdf_files)} PDF files in {directory_path}")
        
        for pdf_file in pdf_files:
            try:
                chunks = self.process_pdf(str(pdf_file))
                all_documents[pdf_file.name] = chunks
                logger.info(f"Successfully processed {pdf_file.name}")
            except Exception as e:
                logger.error(f"Failed to process {pdf_file.name}: {str(e)}")
        
        return all_documents


def ingest_manuals(manuals_dir: str, chunk_size: int = 1024, chunk_overlap: int = 100) -> dict:
    """
    Ingest all manual PDFs from a directory
    
    Args:
        manuals_dir: Directory containing manual PDFs
        chunk_size: Size of chunks
        chunk_overlap: Overlap between chunks
        
    Returns:
        Dictionary of processed documents
    """
    processor = PDFProcessor(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return processor.process_directory(manuals_dir)
