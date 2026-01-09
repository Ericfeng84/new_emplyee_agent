import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import ChatWindow from './components/ChatWindow';
import { api } from './api/client';

function App() {
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // Initialize Session
  useEffect(() => {
    const initSession = async () => {
      try {
        // Check local storage for existing session
        const storedSession = localStorage.getItem('nexus_session_id');
        if (storedSession) {
          setSessionId(storedSession);
          // Load history
          try {
            const history = await api.getSessionHistory(storedSession);
            // Format history
            const formattedMessages = history.map(msg => ({
              role: msg.type === 'human' ? 'user' : 'assistant',
              content: msg.content
            }));
            setMessages(formattedMessages);
          } catch (historyErr) {
            console.warn("Could not load history, creating new session", historyErr);
            await createNewSession();
          }
        } else {
          await createNewSession();
        }
      } catch (err) {
        console.error("Failed to init session:", err);
      }
    };
    initSession();
  }, []);

  const createNewSession = async () => {
    try {
      const data = await api.createSession();
      setSessionId(data.session_id);
      localStorage.setItem('nexus_session_id', data.session_id);
      setMessages([]);
    } catch (err) {
      console.error("Failed to create session:", err);
    }
  };

  const handleSendMessage = async (text) => {
    if (!text.trim() || isLoading) return;

    // Optimistic UI
    const userMsg = { role: 'user', content: text };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      if (!sessionId) {
        // If no session ID for some reason, create one first or fail
        await createNewSession();
      }

      const response = await api.sendMessage(sessionId, text);
      const assistantMsg = {
        role: 'assistant',
        content: response.choices[0].message.content
      };
      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      console.error("Chat error:", err);
      setMessages((prev) => [...prev, {
        role: 'system',
        content: "Error: Failed to get response from agent. Please try again."
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    createNewSession();
  };

  return (
    <div style={{ display: 'flex', height: '100vh', width: '100vw', overflow: 'hidden' }}>
      <Sidebar onNewChat={handleNewChat} />
      <ChatWindow
        messages={messages}
        onSendMessage={handleSendMessage}
      />
    </div>
  );
}

export default App;
