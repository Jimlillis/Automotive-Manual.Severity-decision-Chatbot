// ChatPage.tsx
import React, { useState, useRef, useEffect } from 'react';
import { ArrowLeft, Send } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface Message {
  role: 'user' | 'model';
  text: string;
}

const ChatPage: React.FC = () => {
  const navigate = useNavigate();
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  // Αυτόματο scroll προς τα κάτω σε κάθε νέο μήνυμα
  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { role: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: input,
          history: messages // Στέλνουμε το ιστορικό για να έχει context το AI
        }),
      });

      const data = await response.json();
      
      if (data.reply) {
        setMessages(prev => [...prev, { role: 'model', text: data.reply }]);
      }
    } catch (error) {
      setMessages(prev => [...prev, { role: 'model', text: "❌ Σφάλμα σύνδεσης με τον διακομιστή." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 font-sans">
      {/* Header */}
      <div className="bg-blue-800 text-white p-4 flex items-center shadow-lg">
        <button onClick={() => navigate(-1)} className="mr-4 hover:bg-blue-700 p-1 rounded-full transition">
          <ArrowLeft size={24} />
        </button>
        <h1 className="text-xl font-bold">Insurance Bot (RA & AC)</h1>
      </div>

      {/* Messages Window */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-10">
            Πείτε μας τι συνέβη (π.χ. "Έμεινα από λάστιχο" ή "Τράκαρα")
          </div>
        )}
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] p-3 rounded-2xl shadow ${
              msg.role === 'user' ? 'bg-blue-600 text-white rounded-tr-none' : 'bg-white text-gray-800 rounded-tl-none'
            }`}>
              {msg.text}
            </div>
          </div>
        )}
        {isLoading && <div className="text-sm text-gray-400 animate-pulse">Το AI επεξεργάζεται...</div>}
        <div ref={scrollRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white border-t flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
          placeholder="Γράψτε το μήνυμά σας..."
          className="flex-1 border rounded-full px-4 py-2 focus:ring-2 focus:ring-blue-500 outline-none text-black bg-gray-50"
        />
        <button 
          onClick={handleSendMessage}
          disabled={isLoading}
          className="bg-blue-600 text-white p-3 rounded-full hover:bg-blue-700 disabled:bg-gray-400 transition"
        >
          <Send size={20} />
        </button>
      </div>
    </div>
  );
};

export default ChatPage;