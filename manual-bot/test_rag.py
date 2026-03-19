#!/usr/bin/env python
"""Quick test script for RAG system"""

from app.rag import RAGSystem

# Initialize RAG system
rag = RAGSystem()

# Test question answering
print("Testing question answering with RAG system...")
print("=" * 60)

result = rag.answer_question('How do I open the hood?')

print(f"\nQuestion: How do I open the hood?")
print(f"\nAnswer:\n{result['answer']}")
print(f"\nSources:\n{result['sources']}")
print(f"\nModel: {result['model']}")
print(f"Retrieved chunks: {result.get('retrieved_chunks', 0)}")
