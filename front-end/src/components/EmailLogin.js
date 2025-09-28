import React, { useState } from 'react';
import './EmailLogin.css';

const EmailLogin = ({ onEmailSubmit, onSwitchToSignUp }) => {
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');

  const validateEmail = (email) => {
    return /\S+@\S+\.\S+/.test(email);
  };

  const handleContinue = (e) => {
    e.preventDefault();
    setError('');

    if (!email) {
      setError('Email is required');
      return;
    }

    if (!validateEmail(email)) {
      setError('Please enter a valid email address');
      return;
    }

    // Email is valid, proceed to password module
    onEmailSubmit(email);
  };

  return (
    <div className="email-login-container">
      <form className="email-login-form" onSubmit={handleContinue}>
        <h2>Welcome Back</h2>
        <p className="subtitle">Enter your email to continue</p>
        
        {error && <div className="login-error">{error}</div>}
        
        <div className="form-group">
          <label htmlFor="email">
            Email Address <span className="required">*</span>
          </label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
            className={error ? 'error' : ''}
          />
        </div>
        
        <button type="submit" className="continue-btn">
          Continue <span className="arrow">→</span>
        </button>

        <div className="switch-form">
          <p>Don't have an account?</p>
          <button type="button" className="switch-btn" onClick={onSwitchToSignUp}>
            Sign up here
          </button>
        </div>
      </form>
    </div>
  );
};

export default EmailLogin;