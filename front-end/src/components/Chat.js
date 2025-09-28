import React, { useState, useRef, useEffect } from 'react';
import './Chat.css';
import sparkyGif from '../images/sparkyAI.gif'; // Import the GIF

const Chat = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm Sparky.AI, your favorite SunDevil AI! How can I help you today? Forks Up!",
      sender: 'character',
      timestamp: new Date()
    }
  ]);
  const [inputText, setInputText] = useState('');
  const messagesEndRef = useRef(null);
  
  const MAX_CHARACTERS = 2500;

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = (e) => {
    e.preventDefault();
    
    if (inputText.trim() === '') return;

    // Add user message
    const userMessage = {
      id: messages.length + 1,
      text: inputText,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');

    // Simulate character response after a delay
    setTimeout(() => {
      const characterResponse = {
        id: messages.length + 2,
        text: getCharacterResponse(inputText),
        sender: 'character',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, characterResponse]);
    }, 1000);
  };

  const getCharacterResponse = (userMessage) => {
    const message = userMessage.toLowerCase();
    
    if (message.includes('hello') || message.includes('hi') || message.includes('hey')) {
      return "Hello there! It's great to chat with you! I notice you have plenty of space to type now - feel free to share your thoughts in detail. I'm here to listen and respond to whatever you'd like to discuss.";
    } else if (message.includes('how are you')) {
      return "I'm doing wonderful! Thanks for asking. The new character limit means we can have much more meaningful conversations now. How about you? How has your day been? Feel free to share as much detail as you'd like!";
    } else if (message.includes('name')) {
      return "I'm Sparky.AI, your friendly SunDevil companion! With the increased character limit, we can have proper conversations about names, their meanings, and why they're important to people. What would you like to know about me?";
    } else if (message.includes('help')) {
      return "I'm here to help! Feel free to ask me anything about this application or just chat! Now that you have more space to type, you can describe your questions or concerns in detail, and I'll do my best to provide comprehensive answers that address all aspects of what you're dealing with.";
    } else if (message.includes('thank')) {
      return "You're very welcome! I'm happy to help! It's wonderful that we can now have more substantial conversations without worrying about character limits. This allows for more thoughtful exchanges and deeper understanding between us.";
    } else if (message.includes('weather')) {
      return "I'm not connected to weather services, but I hope it's beautiful where you are! With the expanded character limit, you could describe your local weather in poetic detail if you'd like - the way the light falls through the trees, the temperature on your skin, or how the air smells after rain. I'd love to hear about your environment!";
    } else if (message.includes('joke')) {
      const jokes = [
        "Why don't scientists trust atoms? Because they make up everything! But you know, that's actually a great metaphor for how we perceive reality. Our understanding of the world is built upon fundamental particles that themselves are mostly empty space, yet they create the solid world we experience. It's quite fascinating when you think about it!",
        "Why did the scarecrow win an award? He was outstanding in his field! This joke always makes me think about recognition and how sometimes the most valuable contributions come from those who stand guard over what's important, even if their work isn't always flashy or immediately noticeable.",
        "What do you call a fake noodle? An impasta! Speaking of pasta, have you ever considered how food metaphors permeate our language? We say someone is 'the salt of the earth' or 'the cream of the crop.' It's interesting how nourishment and language are so deeply connected in human culture."
      ];
      return jokes[Math.floor(Math.random() * jokes.length)];
    } else {
      const responses = [
        "That's interesting! Tell me more about that. With the increased character limit, you can really dive deep into your thoughts and share the nuances of your perspective. I'm genuinely curious to understand your viewpoint better.",
        "I see what you mean. What are your thoughts on this? The expanded space for messaging means we can explore topics more thoroughly, examining different angles and considering various implications without feeling rushed or constrained.",
        "Fascinating! I'd love to hear more about your perspective. Now that we're not limited by character counts, you can share the full context, the background story, or the emotional journey behind your thoughts. This makes our conversation much more meaningful.",
        "That's a great point! How did you come to that conclusion? The increased character limit allows you to walk me through your reasoning process step by step, sharing the experiences, observations, or research that led you to this understanding.",
        "I understand. Is there anything specific you'd like to discuss? With 2500 characters available, we can tackle complex topics, share detailed stories, or explore philosophical questions in depth. What would you like to explore together?"
      ];
      return responses[Math.floor(Math.random() * responses.length)];
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
              <div key={message.id} className={`message ${message.sender}`}>
                <div className="message-content">
                  <div className="message-text">{message.text}</div>
                  <div className="message-time">
                    {formatTime(message.timestamp)}
                  </div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          <form className="message-input-form" onSubmit={handleSendMessage}>
            <div className="input-container">
              <textarea
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                placeholder="Type your message here... (You have plenty of space now!)"
                className="message-input"
                maxLength={MAX_CHARACTERS}
                rows={3}
              />
              <button 
                type="submit" 
                className="send-button"
                disabled={!inputText.trim()}
              >
                Send
              </button>
            </div>
            <div className="input-hint">
              Press Enter to send • {MAX_CHARACTERS - inputText.length} characters remaining
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Chat;