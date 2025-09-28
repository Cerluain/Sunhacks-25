// Updated App.js with Chat component
import React, { useState } from 'react';
import './App.css';
import Login from './components/Login';
import Header from './components/Header';
import Homepage from './components/Homepage';
import Chat from './components/Chat'; // Add this import

function App() {
  const [user, setUser] = useState(null);
  const [showLogin, setShowLogin] = useState(false);
  const [currentView, setCurrentView] = useState('home'); // 'home', 'login', 'chat'

  const handleLoginClick = () => {
    setCurrentView('login');
    setShowLogin(true);
  };

  const handleHomeClick = () => {
    setCurrentView('home');
    setShowLogin(false);
  };

  const handleChatClick = () => {
    if (user) {
      setCurrentView('chat');
    } else {
      setCurrentView('login');
      setShowLogin(true);
    }
  };

  const handleLogin = (userData) => {
    setUser(userData);
    setShowLogin(false);
    setCurrentView('home');
  };

  const handleLogout = () => {
    setUser(null);
    setShowLogin(false);
    setCurrentView('home');
  };

  const renderContent = () => {
    if (showLogin || currentView === 'login') {
      return <Login onLogin={handleLogin} />;
    }
    
    if (currentView === 'chat') {
      return <Chat />;
    }
    
    if (user) {
      return (
        <header className="App-header">
          <h1>Welcome{user.isAdmin ? ' Admin' : ''}, {user.email} 🎉</h1>
          <p>You are now logged in to the demo app.</p>
          {user.isAdmin && (
            <div className="admin-badge">
              🔑 Administrator Access
            </div>
          )}
          <div className="action-buttons">
            <button className="chat-btn" onClick={handleChatClick}>
              💬 Start Chatting
            </button>
            <button className="logout-btn" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </header>
      );
    }
    
    return <Homepage />;
  };

  return (
    <div className="App">
      <Header 
        user={user}
        onLoginClick={handleLoginClick}
        onLogout={handleLogout}
        onHomeClick={handleHomeClick}
        onChatClick={handleChatClick}
      />
      
      {renderContent()}
    </div>
  );
}

export default App;