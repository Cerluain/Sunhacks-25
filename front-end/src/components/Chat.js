import React, { useState, useRef, useEffect } from 'react';
import './Chat.css';
import sparkyGif from '../images/sparkyAI.gif'; // Import the GIF
import { chatAPI, handleAPIError, authAPI } from '../services/api';

const Chat = ({ user }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm Sparky.AI, your favorite SunDevil AI! How can I help you today? Forks Up!",
      sender: 'character',
      timestamp: new Date(),
      isWelcome: true
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const messagesEndRef = useRef(null);
  
  const MAX_CHARACTERS = 1000; // Match backend limit

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (inputText.trim() === '' || isLoading) return;

    // Clear any previous errors
    setError('');

    // Add user message
    const userMessage = {
      id: Date.now(),
      text: inputText.trim(),
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputText.trim();
    setInputText('');
    setIsLoading(true);

    try {
      // Check if user is still authenticated
      if (!authAPI.isLoggedIn()) {
        throw new Error('Your session has expired. Please log in again.');
      }

      // Call the backend API
      const response = await chatAPI.askQuestion(currentInput, true);

      // Add AI response
      const aiMessage = {
        id: Date.now() + 1,
        text: response.answer.join('\n'), // Backend returns answer as array of strings
        sender: 'character',
        timestamp: new Date(),
        sources: response.sources || []
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage = handleAPIError(error);
      setError(errorMessage);
      
      // Add error message to chat
      const errorChatMessage = {
        id: Date.now() + 1,
        text: `Sorry, I encountered an error: ${errorMessage}`,
        sender: 'character',
        timestamp: new Date(),
        isError: true
      };
      setMessages(prev => [...prev, errorChatMessage]);
    } finally {
      setIsLoading(false);
    }
  };



  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="chat-container">
      <div className="chat-layout">
        {/* Character Section */}
        <div className="character-section">
          <div className="character-image-placeholder">
            <div className="character-image">
              <img src={sparkyGif} alt="Sparky.AI Mascot" />
            </div>
            <div className="character-info">
              <h3>Sparky.AI</h3>
              <p>Your AI Companion</p>
              <div className="character-status">
                <span className="status-indicator"></span>
                Online
              </div>
            </div>
          </div>
          
          <div className="character-description">
            <h4>About Me</h4>
            <p>
              I'm here to make your academic journey easier by helping you find resources, stay organized, and connect with your community at ASU. Whether you need quick answers, study support, or just someone to chat with, I've got you covered!
            </p>
          </div>
        </div>

        {/* Chat Section */}
        <div className="chat-section">
          <div className="chat-header">
            <h2>Conversation with Sparky.AI</h2>
          </div>

          <div className="messages-container">
            {messages.map((message) => (
              <div key={message.id} className={`message ${message.sender} ${message.isError ? 'error' : ''}`}>
                <div className="message-content">
                  <div className="message-text">{message.text}</div>
                  {message.sources && message.sources.length > 0 && (
                    <div className="message-sources">
                      <p><strong>Sources:</strong></p>
                      <ul>
                        {message.sources.map((source, index) => (
                          <li key={index}>
                            <a href={source.url} target="_blank" rel="noopener noreferrer">
                              {source.url}
                            </a>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                  <div className="message-time">
                    {formatTime(message.timestamp)}
                  </div>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message character loading">
                <div className="message-content">
                  <div className="message-text">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                    Sparky is thinking...
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {error && (
            <div className="chat-error">
              <p><strong>Connection Error:</strong> {error}</p>
              <button onClick={() => setError('')}>Dismiss</button>
            </div>
          )}

          <form className="message-input-form" onSubmit={handleSendMessage}>
            <div className="input-container">
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder={
                  user?.isDemoAdmin 
                    ? "Demo mode: Ask me anything about ASU!" 
                    : "Ask me anything about ASU! I'm connected to real AI."
                }
                className="message-input"
                maxLength={MAX_CHARACTERS}
                rows={3}
                disabled={isLoading}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSendMessage(e);
                  }
                }}
              />
              <button 
                type="submit" 
                className="send-button"
                disabled={!inputText.trim() || isLoading}
              >
                {isLoading ? '...' : 'Send'}
              </button>
            </div>
            <div className="input-hint">
              {isLoading 
                ? 'Sending message to AI...' 
                : `Press Enter to send • ${MAX_CHARACTERS - inputText.length} characters remaining`
              }
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Chat;