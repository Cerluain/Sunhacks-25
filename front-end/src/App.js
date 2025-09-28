// Updated App.js with Chat component
import React, { useState, useEffect } from 'react';
import './App.css';
import Login from './components/Login';
import Header from './components/Header';
import Homepage from './components/Homepage';
import Chat from './components/Chat'; // Add this import
import { authAPI } from './services/api';

function App() {
  const [user, setUser] = useState(null);
  const [showLogin, setShowLogin] = useState(false);
  const [currentView, setCurrentView] = useState('home'); // 'home', 'login', 'chat'
  const [isLoading, setIsLoading] = useState(true);

  // Check for existing authentication on app load
  useEffect(() => {
    const checkAuthStatus = () => {
      if (authAPI.isLoggedIn()) {
        const userInfo = authAPI.getCurrentUser();
        if (userInfo) {
          setUser({
            email: userInfo.email,
            id: userInfo.user_id,
            isAdmin: userInfo.is_admin
          });
        }
      }
      setIsLoading(false);
    };

    checkAuthStatus();
  }, []);

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

  const handleLogout = async () => {
    try {
      await authAPI.logout(); // This now calls backend and clears local storage
    } catch (error) {
      console.warn('Logout error (token already cleared):', error);
    }
    setUser(null);
    setShowLogin(false);
    setCurrentView('home');
  };

  const renderContent = () => {
    if (isLoading) {
      return (
        <div className="App-header">
          <h1>Loading...</h1>
          <p>Checking authentication status...</p>
        </div>
      );
    }

    if (showLogin || currentView === 'login') {
      return <Login onLogin={handleLogin} />;
    }
    
    if (currentView === 'chat') {
      return <Chat user={user} />;
    }
    
    if (user) {
      return (
        <header className="App-header">
          <h1>Welcome{user.isAdmin ? ' Admin' : ''}, {user.email} 🎉</h1>
          <p>You are now logged in and connected to the backend API.</p>
          {user.isAdmin && (
            <div className="admin-badge">
              🔑 Administrator Access - Full System Privileges
            </div>
          )}
          <div className="action-buttons">
            <button className="chat-btn" onClick={handleChatClick}>
              💬 Start Chatting with AI
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