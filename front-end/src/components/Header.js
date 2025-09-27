import React from 'react';
import './Header.css';

const Header = ({ user, onLoginClick, onLogout, onHomeClick }) => {
  return (
    <header className="header">
      <div className="header-left">
        <h1 className="company-name">SunHacks</h1>
      </div>
      
      <div className="header-right">
        <button className="header-btn home-btn" onClick={onHomeClick}>
          Home
        </button>
        
        {user ? (
          <div className="user-section">
            <span className="user-email">Welcome, {user.email}</span>
            <button className="header-btn logout-btn" onClick={onLogout}>
              Logout
            </button>
          </div>
        ) : (
          <button className="header-btn login-btn" onClick={onLoginClick}>
            Login / Sign Up
          </button>
        )}
      </div>
    </header>
  );
};

export default Header;