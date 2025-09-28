import React, { useState } from 'react';
import SignUp from './SignUp';
import './Login.css';

const Login = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    // Simple validation
    if (!email || !password) {
      setError('Please fill in all fields');
      return;
    }

    // Basic email validation
    if (!email.includes('@')) {
      setError('Please enter a valid email address');
      return;
    }

    // Simulate login success
    onLogin({ email });
  };

  const handleSignUp = (userData) => {
    // After successful sign up, automatically log the user in
    onLogin(userData);
  };

  if (isSignUp) {
    return <SignUp onSignUp={handleSignUp} onSwitchToLogin={() => setIsSignUp(false)} />;
  }

  return (
    <div className="login-container">
      <form className="login-form" onSubmit={handleSubmit}>
        <h2>Login</h2>
        
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
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="password">
            Password <span className="required">*</span>
          </label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
          />
        </div>
        
        <button type="submit" className="login-btn">
          Login
        </button>

        <div className="switch-form">
          <p>Don't have an account?</p>
          <button type="button" className="switch-btn" onClick={() => setIsSignUp(true)}>
            Sign up here
          </button>
        </div>
      </form>
    </div>
  );
};

export default Login;