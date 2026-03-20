"""
FastAPI backend for Automotive Manual ChatBot
"""

import logging
import asyncio
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import shutil

from app.rag import RAGSystem
from app.config import settings
from app.utils import ensure_directory_exists

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered chatbot for vehicle manual assistance"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system
rag_system: Optional[RAGSystem] = None


# Pydantic models
class QuestionRequest(BaseModel):
    """Request model for questions"""
    question: str = Field(..., description="User question about the vehicle manual")
    top_k: Optional[int] = Field(8, description="Maximum number of chunks to retrieve before filtering")


class AnswerResponse(BaseModel):
    """Response model for answers"""
    answer: str = Field(..., description="Generated answer")
    sources: str = Field(..., description="Source page references")
    retrieved_chunks: int = Field(..., description="Number of chunks retrieved")
    model: str = Field(..., description="LLM model used")
    tokens_used: int = Field(..., description="Tokens used in generation")


class StatusResponse(BaseModel):
    """Status response model"""
    status: str = Field(..., description="Current status")
    message: str = Field(..., description="Status message")
    ready: bool = Field(..., description="Whether system is ready")


class UploadResponse(BaseModel):
    """File upload response"""
    filename: str = Field(..., description="Uploaded filename")
    size: int = Field(..., description="File size in bytes")
    message: str = Field(..., description="Upload status message")


class IngestResponse(BaseModel):
    """Manual ingestion response"""
    documents_ingested: int = Field(..., description="Number of documents ingested")
    message: str = Field(..., description="Ingestion status message")


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize RAG system on startup"""
    global rag_system
    try:
        # Ensure required directories exist
        ensure_directory_exists(settings.CHROMA_DB_PATH)
        ensure_directory_exists(str(settings.MANUALS_DIR))
        
        # Initialize RAG system
        rag_system = RAGSystem(
        db_path=settings.CHROMA_DB_PATH
        )
        
        logger.info("RAG system initialized successfully")
        
        # Auto-ingest existing manuals if any
        if settings.MANUALS_DIR.exists():
            manual_count = len(list(settings.MANUALS_DIR.glob("*.pdf")))
            if manual_count > 0:
                logger.info(f"Found {manual_count} existing manuals. Starting ingestion...")
                try:
                    await asyncio.to_thread(
                        rag_system.ingest_manuals,
                        str(settings.MANUALS_DIR)
                    )
                    logger.info("Existing manuals ingested successfully")
                except Exception as e:
                    logger.warning(f"Could not ingest existing manuals: {str(e)}")
        
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down application")


# API Endpoints
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health", response_model=StatusResponse, tags=["Health"])
async def health_check():
    """Check system health and readiness"""
    if rag_system is None:
        raise HTTPException(
            status_code=500,
            detail="RAG system not initialized"
        )
    
    return StatusResponse(
        status="healthy",
        message="System is operational",
        ready=True
    )


@app.post("/ask", response_model=AnswerResponse, tags=["QA"])
async def ask_question(request: QuestionRequest):
    """
    Ask a question about vehicle manuals
    
    The system will retrieve relevant manual sections and generate an answer
    using the LLM with those sections as context.
    """
    if rag_system is None:
        raise HTTPException(
            status_code=500,
            detail="RAG system not initialized"
        )
    
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )
    
    try:
        # Run RAG pipeline in thread pool to avoid blocking
        result = await asyncio.to_thread(
            rag_system.answer_question,
            request.question,
            request.top_k
        )
        
        return AnswerResponse(
            answer=result["answer"],
            sources=result["sources"],
            retrieved_chunks=result["retrieved_chunks"],
            model=result["model"],
            tokens_used=result["tokens_used"]
        )
        
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )


@app.get("/retrieve", tags=["QA"])
async def retrieve_documents(query: str, top_k: int = 8):
    """
    Retrieve relevant documents for a query without generating an answer
    
    Useful for debugging and understanding what documents are retrieved.
    """
    if rag_system is None:
        raise HTTPException(
            status_code=500,
            detail="RAG system not initialized"
        )
    
    if not query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty"
        )
    
    try:
        documents = await asyncio.to_thread(
            rag_system.retrieve,
            query,
            top_k
        )
        
        return {
            "query": query,
            "retrieved_count": len(documents),
            "documents": documents
        }
        
    except Exception as e:
        logger.error(f"Error retrieving documents: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving documents: {str(e)}"
        )


@app.post("/upload-manual", response_model=UploadResponse, tags=["Manuals"])
async def upload_manual(file: UploadFile = File(...)):
    """
    Upload a vehicle manual PDF
    
    The PDF will be stored and can be ingested into the knowledge base.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted"
        )
    
    try:
        # Ensure directory exists
        ensure_directory_exists(str(settings.MANUALS_DIR))
        
        # Save file
        file_path = settings.MANUALS_DIR / file.filename
        
        with open(file_path, "wb") as buffer:
            contents = await file.read()
            buffer.write(contents)
        
        file_size = len(contents)
        logger.info(f"Uploaded manual: {file.filename} ({file_size} bytes)")
        
        return UploadResponse(
            filename=file.filename,
            size=file_size,
            message=f"File {file.filename} uploaded successfully. Use /ingest to add to knowledge base."
        )
        
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error uploading file: {str(e)}"
        )


@app.post("/ingest", response_model=IngestResponse, tags=["Manuals"])
async def ingest_manuals():
    """
    Ingest all PDF manuals from the manuals directory
    
    This will process all PDFs and add them to the vector database.
    Can take some time for large manuals.
    """
    if rag_system is None:
        raise HTTPException(
            status_code=500,
            detail="RAG system not initialized"
        )
    
    if not settings.MANUALS_DIR.exists():
        raise HTTPException(
            status_code=400,
            detail="Manuals directory does not exist"
        )
    
    try:
        # Run ingestion in thread pool
        document_count = await asyncio.to_thread(
            rag_system.ingest_manuals,
            str(settings.MANUALS_DIR)
        )
        
        return IngestResponse(
            documents_ingested=document_count,
            message=f"Successfully ingested {document_count} document chunks"
        )
        
    except Exception as e:
        logger.error(f"Error during ingestion: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error during ingestion: {str(e)}"
        )


@app.delete("/clear-database", tags=["Manuals"])
async def clear_database():
    """
    Clear the vector database
    
    WARNING: This will delete all ingested documents. Use with caution!
    """
    if rag_system is None:
        raise HTTPException(
            status_code=500,
            detail="RAG system not initialized"
        )
    
    try:
        await asyncio.to_thread(rag_system.vector_db.clear)
        logger.info("Vector database cleared")
        
        return {
            "status": "success",
            "message": "Vector database cleared successfully"
        }
        
    except Exception as e:
        logger.error(f"Error clearing database: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error clearing database: {str(e)}"
        )


@app.get("/config", tags=["System"])
async def get_config():
    """Get current system configuration (non-sensitive)"""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "model": settings.OLLAMA_MODEL,
        "chunk_size": settings.CHUNK_SIZE,
        "chunk_overlap": settings.CHUNK_OVERLAP,
        "top_k_chunks": settings.TOP_K_CHUNKS,
        "temperature": settings.TEMPERATURE,
        "max_tokens": settings.MAX_TOKENS
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP Exception: {exc.detail}")
    return {
        "detail": exc.detail,
        "status_code": exc.status_code
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG
    )
