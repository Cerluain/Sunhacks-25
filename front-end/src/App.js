// Updated App.js
import React, { useState } from 'react';
import './App.css';
import Login from './components/Login';
import Header from './components/Header';
import Homepage from './components/Homepage';

function App() {
  const [user, setUser] = useState(null);
  const [showLogin, setShowLogin] = useState(false);

  const handleLoginClick = () => {
    setShowLogin(true);
  };

  const handleHomeClick = () => {
    setShowLogin(false);
  };

  const handleLogin = (userData) => {
    setUser(userData);
    setShowLogin(false);
  };

  const handleLogout = () => {
    setUser(null);
    setShowLogin(false);
  };

  return (
    <div className="App">
      <Header 
        user={user}
        onLoginClick={handleLoginClick}
        onLogout={handleLogout}
        onHomeClick={handleHomeClick}
      />
      
      {showLogin ? (
        <Login onLogin={handleLogin} />
      ) : user ? (
        <header className="App-header">
          <h1>Welcome{user.isAdmin ? ' Admin' : ''}, {user.email} 🎉</h1>
          <p>You are now logged in to the demo app.</p>
          {user.isAdmin && (
            <div className="admin-badge">
              🔑 Administrator Access
            </div>
          )}
          <button className="logout-btn" onClick={handleLogout}>
            Logout
          </button>
        </header>
      ) : (
        <Homepage />
      )}
    </div>
  );
}

export default App;