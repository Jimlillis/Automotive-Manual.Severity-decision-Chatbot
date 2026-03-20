#!/usr/bin/env python
"""Interactive CLI for the Automotive Manual ChatBot"""

from app.rag import RAGSystem

def main():
    print("=" * 60)
    print("🚗 Automotive Manual ChatBot - Interactive Mode")
    print("=" * 60)
    print("Type your questions about the vehicle manual.")
    print("Type 'quit' or 'exit' to exit.\n")
    
    # Initialize RAG system
    print("Loading manual database...")
    rag = RAGSystem()
    print("✅ Ready to answer questions!\n")
    
    while True:
        try:
            question = input("You: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye! 👋")
                break
            
            print("\n🔍 Searching manual database...")
            result = rag.answer_question(question)
            
            print(f"\n🤖 Bot: {result['answer']}")
            print(f"\n📌 Sources: {result['sources']}")
            print(f"📊 Model: {result['model']} | Chunks retrieved: {result.get('retrieved_chunks', 0)}")
            print("\n" + "-" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}\n")

if __name__ == "__main__":
    main()
