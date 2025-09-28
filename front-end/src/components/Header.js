// components/Header.js
import React from 'react';
import './Header.css';

const Header = ({ user, onLoginClick, onLogout, onHomeClick }) => {
  return (
    <header className="app-header">
      <div className="header-content">
        <div className="company-name">SunHacks</div>
        <nav className="header-nav">
          <div className="button-group">
            <button className="nav-button home-btn" onClick={onHomeClick}>
              Home
            </button>
            {user ? (
              <button className="nav-button auth-btn logout-btn" onClick={onLogout}>
                Logout
              </button>
            ) : (
              <button className="nav-button auth-btn login-btn" onClick={onLoginClick}>
                Login / Sign Up
              </button>
            )}
          </div>
        </nav>
      </div>
    </header>
  );
};

export default Header;