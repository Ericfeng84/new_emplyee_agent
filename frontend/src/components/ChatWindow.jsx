import React, { useState, useRef, useEffect } from 'react';
import { Send, Paperclip, MoreVertical } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import styles from './ChatWindow.module.css';

const ChatWindow = ({ messages, onSendMessage }) => {
    const [inputValue, setInputValue] = useState('');
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = () => {
        if (inputValue.trim()) {
            onSendMessage(inputValue);
            setInputValue('');
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <main className={styles.chatWindow}>
            <header className={styles.header}>
                <div className={styles.headerInfo}>
                    <h2 className={styles.title}>Nexus Assistant</h2>
                    <span className={styles.status}>Online</span>
                </div>
                <button className={styles.actionBtn}>
                    <MoreVertical size={20} />
                </button>
            </header>

            <div className={styles.messagesArea}>
                {messages.length === 0 ? (
                    <div className={styles.emptyState}>
                        <h1>How can I help you today?</h1>
                        <p>Ask about company policies, IT support, or your benefits.</p>
                    </div>
                ) : (
                    messages.map((msg, index) => (
                        <div
                            key={index}
                            className={`${styles.message} ${msg.role === 'user' ? styles.userMessage : styles.agentMessage
                                }`}
                        >
                            <div className={styles.messageContent}>
                                {msg.role === 'assistant' ? (
                                    <ReactMarkdown>{msg.content}</ReactMarkdown>
                                ) : (
                                    msg.content
                                )}
                            </div>
                            <div className={styles.messageTime}>
                                {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </div>
                        </div>
                    ))
                )}
                <div ref={messagesEndRef} />
            </div>

            <div className={styles.inputArea}>
                <div className={styles.inputContainer}>
                    <button className={styles.attachBtn}>
                        <Paperclip size={20} />
                    </button>
                    <textarea
                        className={styles.input}
                        placeholder="Type your message..."
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyDown={handleKeyPress}
                        rows={1}
                    />
                    <button
                        className={`${styles.sendBtn} ${inputValue.trim() ? styles.active : ''}`}
                        onClick={handleSend}
                        disabled={!inputValue.trim()}
                    >
                        <Send size={18} />
                    </button>
                </div>
            </div>
        </main>
    );
};

export default ChatWindow;
