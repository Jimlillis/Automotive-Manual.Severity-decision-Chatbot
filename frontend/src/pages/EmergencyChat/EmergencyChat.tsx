// ChatPage.tsx
import React, { useState, useRef, useEffect } from 'react';
import { ArrowLeft, Send, Sparkles, User as UserIcon } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import styles from './EmergencyChat.module.css';

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

  const handleSendMessage = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
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
        setMessages(prev => [...prev, { role: 'model', text: data.reply }]); // Προσθέτουμε την απάντηση του μοντέλου στα μηνύματα
      }
    } catch {
      setMessages(prev => [...prev, { role: 'model', text: "❌ Σφάλμα σύνδεσης με τον διακομιστή." }]);
    } finally {
      setIsLoading(false);
    }
  };

return (
    <div className={styles.pageContainer}>
      
      {/* Header */}
      <header className={styles.header}>
        <button onClick={() => navigate(-1)} className={styles.backButton}>
          <ArrowLeft size={24} />
        </button>
        <h1 className={styles.title}>Insurance Bot (RA & AC)</h1>
      </header>

      {/* Κεντρικό Chat Container */}
      <main className={styles.chatContainer}>
        
        {/* Messages Window */}
        <div className={styles.messagesArea}>
          
          {/* Μήνυμα όταν το chat είναι άδειο */}
          {messages.length === 0 && (
            <div style={{ textAlign: 'center', color: '#64748b', marginTop: '20px' }}>
              Πείτε μας τι συνέβη (π.χ. "Έμεινα από λάστιχο" ή "Τράκαρα")
            </div>
          )}

          {/* Λίστα Μηνυμάτων */}
          {messages.map((msg, idx) => (
            <div 
              key={idx} 
              className={`${styles.messageWrapper} ${msg.role === 'user' ? styles.wrapperUser : styles.wrapperBot}`}
            >
              {/* Εικονίδιο Bot (αν το μήνυμα είναι από το μοντέλο) */}
              {msg.role === 'model' && (
                <div className={styles.botIconWrapper}>
                  <Sparkles size={20} className={styles.botIcon} />
                </div>
              )}

              {/* Το συννεφάκι */}
              <div className={`${styles.messageBubble} ${msg.role === 'user' ? styles.bubbleUser : styles.bubbleBot}`}>
                <p>{msg.text}</p>
              </div>

              {/* Εικονίδιο User (αν το μήνυμα είναι από τον χρήστη) */}
              {msg.role === 'user' && (
                <div className={styles.userIconWrapper}>
                  <UserIcon size={20} className={styles.userIcon} />
                </div>
              )}
            </div>
          ))}

          {/* Loading State (Εμφανίζεται σαν μήνυμα από το bot) */}
          {isLoading && (
            <div className={`${styles.messageWrapper} ${styles.wrapperBot}`}>
              <div className={styles.botIconWrapper}>
                <Sparkles size={20} className={styles.botIcon} />
              </div>
              <div className={`${styles.messageBubble} ${styles.bubbleBot}`}>
                <p style={{ opacity: 0.7 }}>Το AI επεξεργάζεται...</p>
              </div>
            </div>
          )}
          
          <div ref={scrollRef} />
        </div>

        {/* Input Area */}
        <div className={styles.inputArea}>
          {/* Χρησιμοποιούμε form για να λειτουργεί σωστά το Enter */}
          <form className={styles.inputForm} onSubmit={handleSendMessage}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Γράψτε το μήνυμά σας..."
              className={styles.inputField}
              disabled={isLoading}
            />
            <button 
              type="submit" 
              className={styles.sendButton} 
              disabled={isLoading || !input.trim()}
            >
              <Send size={20} className={styles.sendIcon} />
            </button>
          </form>
        </div>
      </main>

    </div>
  );
};

export default ChatPage;