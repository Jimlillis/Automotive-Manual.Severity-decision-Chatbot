"""
RAG (Retrieval-Augmented Generation) system for answering questions using vehicle manuals
"""

import logging
from typing import List, Dict, Any, Optional
import chromadb
import requests

from app.config import settings
from app.ingest import ingest_manuals
from app.prompts import get_system_message, get_context_prompt
from app.utils import clean_text, format_context, format_sources

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorDatabase:
    """Wrapper for Chroma vector database"""
    
    def __init__(self, db_path: str, collection_name: str = "automotive_manuals"):
        """
        Initialize Chroma vector database
        
        Args:
            db_path: Path to store vector database
            collection_name: Name of the collection
        """
        self.db_path = db_path
        self.collection_name = collection_name
        
        # Initialize Chroma client (new API)
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info(f"Initialized vector database at {db_path}")
    
    def add_documents(self, documents: List[dict], batch_size: int = 100) -> None:
        """
        Add documents to the vector database
        
        Args:
            documents: List of document chunks with content and metadata
            batch_size: Batch size for adding documents
        """
        total_added = 0
        
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            
            ids = [f"doc_{hash(batch[j]['content'])}_{j}" for j in range(len(batch))]
            documents_text = [doc["content"] for doc in batch]
            metadatas = [{
                "page": doc["page"],
                "source": doc.get("source", ""),
                "chunk_id": doc.get("chunk_id", "")
            } for doc in batch]
            
            try:
                self.collection.add(
                    ids=ids,
                    documents=documents_text,
                    metadatas=metadatas
                )
                total_added += len(batch)
                logger.info(f"Added {total_added} documents to database")
            except Exception as e:
                logger.error(f"Error adding documents to database: {str(e)}")
                raise
    
    def search(self, query: str, top_k: int = 5) -> List[dict]:
        """
        Search for relevant documents
        
        Args:
            query: Search query
            top_k: Number of top results to return
            
        Returns:
            List of relevant documents with metadata
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k
            )
            
            # Format results
            documents = []
            if results and results["documents"] and len(results["documents"]) > 0:
                for i, doc in enumerate(results["documents"][0]):
                    metadata = results["metadatas"][0][i] if results["metadatas"] and len(results["metadatas"]) > 0 else {}
                    documents.append({
                        "content": doc,
                        "page": metadata.get("page", "Unknown"),
                        "distance": results["distances"][0][i] if results["distances"] and len(results["distances"]) > 0 else None
                    })
            
            logger.info(f"Found {len(documents)} relevant documents for query")
            return documents
            
        except Exception as e:
            logger.error(f"Error searching database: {str(e)}")
            return []
    
    def clear(self) -> None:
        """Clear all documents from the collection"""
        try:
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("Cleared vector database")
        except Exception as e:
            logger.error(f"Error clearing database: {str(e)}")


class RAGSystem:
    """Main RAG system combining retrieval and generation"""
    
    def __init__(self, db_path: str = None):
        """
        Initialize RAG system
        
        Args:
            db_path: Path to vector database
        """
        self.db_path = db_path or settings.CHROMA_DB_PATH
        self.ollama_base_url = settings.OLLAMA_BASE_URL
        self.ollama_model = settings.OLLAMA_MODEL
        
        # Initialize vector database
        self.vector_db = VectorDatabase(self.db_path, settings.COLLECTION_NAME)
        
        self.temperature = settings.TEMPERATURE
        self.max_tokens = settings.MAX_TOKENS
        
        logger.info(f"Initialized RAG system with Ollama model: {self.ollama_model}")
        logger.info(f"Ollama URL: {self.ollama_base_url}")
    
    def ingest_manuals(self, manuals_dir: str) -> int:
        """
        Ingest vehicle manuals into the system
        
        Args:
            manuals_dir: Directory containing manual PDFs
            
        Returns:
            Number of documents added
        """
        logger.info(f"Starting manual ingestion from {manuals_dir}")
        
        try:
            # Process PDFs
            all_documents = ingest_manuals(
                manuals_dir,
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP
            )
            
            # Flatten documents for database
            documents_list = []
            for filename, chunks in all_documents.items():
                for chunk in chunks:
                    chunk["filename"] = filename
                    documents_list.append(chunk)
            
            # Add to vector database
            if documents_list:
                self.vector_db.add_documents(documents_list)
                logger.info(f"Successfully ingested {len(documents_list)} document chunks")
                return len(documents_list)
            else:
                logger.warning("No documents found to ingest")
                return 0
                
        except Exception as e:
            logger.error(f"Error during manual ingestion: {str(e)}")
            raise
    
    def retrieve(self, query: str, top_k: int = None) -> List[dict]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: User query
            top_k: Number of top results
            
        Returns:
            List of relevant documents
        """
        top_k = top_k or settings.TOP_K_CHUNKS
        return self.vector_db.search(query, top_k=top_k)
    
    def generate_answer(self, question: str, context_documents: List[dict]) -> Dict[str, Any]:
        """
        Generate an answer using retrieved documents with Ollama
        
        Args:
            question: User question
            context_documents: Retrieved context documents
            
        Returns:
            Answer with metadata
        """
        try:
            # Format context
            if not context_documents:
                return {
                    "answer": "I couldn't find relevant information in the manuals to answer your question.",
                    "sources": "No relevant manual sections found",
                    "model": self.ollama_model,
                    "tokens_used": 0
                }
            
            context = format_context(context_documents)
            sources = format_sources(context_documents)
            
            # Prepare messages
            system_message = get_system_message()
            user_message = get_context_prompt(context, question)
            
            # Call Ollama via API
            payload = {
                "model": self.ollama_model,
                "messages": [
                    {"role": "system", "content": system_message["content"]},
                    {"role": "user", "content": user_message}
                ],
                "stream": False,
                "temperature": self.temperature
            }
            
            response = requests.post(
                f"{self.ollama_base_url}/api/chat",
                json=payload,
                timeout=120
            )
            
            response.raise_for_status()
            data = response.json()
            answer = data["message"]["content"]
            
            logger.info(f"Generated answer using Ollama model: {self.ollama_model}")
            
            return {
                "answer": answer,
                "sources": sources,
                "model": self.ollama_model,
                "tokens_used": 0
            }
            
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            return {
                "answer": f"Error generating answer: {str(e)}",
                "sources": "",
                "model": self.ollama_model,
                "tokens_used": 0
            }
    
    def answer_question(self, question: str, top_k: int = None) -> Dict[str, Any]:
        """
        Complete pipeline: retrieve documents and generate answer
        
        Args:
            question: User question
            top_k: Number of top results to retrieve
            
        Returns:
            Complete answer with metadata
        """
        logger.info(f"Processing question: {question}")
        
        # Retrieve relevant documents
        documents = self.retrieve(question, top_k=top_k)
        
        # Generate answer
        result = self.generate_answer(question, documents)
        result["retrieved_chunks"] = len(documents)
        
        return result
