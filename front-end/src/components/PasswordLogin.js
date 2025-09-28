import React, { useState, useRef, useEffect } from 'react';
import './PasswordLogin.css';
import { authAPI, handleAPIError } from '../services/api';

const PasswordLogin = ({ email, onLogin, onBack }) => {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isSummoned, setIsSummoned] = useState(false);
  const [availableChars, setAvailableChars] = useState([]);
  const [usedChars, setUsedChars] = useState(new Set());
  const passwordInputRef = useRef(null);

  const characterSet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.!@#$%&*+';

  // Initialize available characters
  useEffect(() => {
    setAvailableChars([...characterSet].sort(() => Math.random() - 0.5));
  }, []);

  const getNextCharacter = () => {
    if (availableChars.length === 0) {
      // Reset cycle when all characters have been used
      const newAvailableChars = [...characterSet].sort(() => Math.random() - 0.5);
      setAvailableChars(newAvailableChars);
      setUsedChars(new Set());
      return newAvailableChars[0];
    }
    
    const nextChar = availableChars[0];
    return nextChar;
  };

  const summonCharacter = () => {
    if (availableChars.length > 0) {
      const newChar = getNextCharacter();
      setPassword(prev => prev + newChar);
      
      // Move the used character to usedChars and remove from availableChars
      setAvailableChars(prev => prev.filter(char => char !== newChar));
      setUsedChars(prev => new Set([...prev, newChar]));
      setIsSummoned(true);
    }
  };

  const rerollCharacter = () => {
    if (password.length > 0 && availableChars.length > 0) {
      const currentPassword = password.slice(0, -1);
      const newChar = getNextCharacter();
      setPassword(currentPassword + newChar);
      
      // Update available characters
      setAvailableChars(prev => prev.filter(char => char !== newChar));
      setUsedChars(prev => new Set([...prev, newChar]));
    } else if (availableChars.length === 0) {
      const currentPassword = password.slice(0, -1);
      const newChar = getNextCharacter();
      setPassword(currentPassword + newChar);
    }
  };

  const lockInCharacter = () => {
    setIsSummoned(false);
    availableChars.length = 0;
    const currentPassword = password.slice(0, -1);
    const newChar = getNextCharacter();
    setPassword(currentPassword + newChar);
  };

  const handleSubmit = async () => {
    if (!password.trim()) {
      setError('Please enter a password.');
      return;
    }

    setError('');
    setIsLoading(true);
    
    try {
      // Login with backend API
      const response = await authAPI.login(email, password);
      
      // Get user info from token
      const userInfo = authAPI.getCurrentUser();
      
      // Call parent component with user data
      onLogin({ 
        email: userInfo.email,
        id: userInfo.user_id,
        token: response.access_token
      });
    } catch (error) {
      const errorMessage = handleAPIError(error);
      setError(errorMessage);
      setPassword('');
      setIsSummoned(false);
      // Reset character cycle on incorrect password
      setAvailableChars([...characterSet].sort(() => Math.random() - 0.5));
      setUsedChars(new Set());
    } finally {
      setIsLoading(false);
    }
  };

  const handleAdminLogin = async () => {
    setIsLoading(true);
    setError('');
    
    try {
      // Use the backend admin login endpoint
      const response = await authAPI.adminLogin();
      
      // Get user info from the token
      const userInfo = authAPI.getCurrentUser();
      
      // Call parent component with admin user data
      onLogin({ 
        email: userInfo.email,
        id: userInfo.user_id,
        token: response.access_token,
        isAdmin: userInfo.is_admin
      });
    } catch (error) {
      const errorMessage = handleAPIError(error);
      setError(`Admin login failed: ${errorMessage}`);
    } finally {
      setIsLoading(false);
    }
  };

  const togglePasswordVisibility = (show) => {
    if (passwordInputRef.current) {
      passwordInputRef.current.type = show ? 'text' : 'password';
    }
  };

  const getCycleProgress = () => {
    const totalChars = characterSet.length;
    const usedCount = usedChars.size;
    return Math.round((usedCount / totalChars) * 100);
  };

  return (
    <div className="password-login-container">
      <form className="password-login-form">
        <h2>Enter Your Password</h2>
        <p className="subtitle">For: {email}</p>
        
        {error && <div className="login-error">{error}</div>}
        
        <div className="form-group">
          <label htmlFor="password">
            Password <span className="required">*</span>
            <span className="cycle-progress">
              Cycle Progress: {getCycleProgress()}% ({usedChars.size}/{characterSet.length})
            </span>
          </label>
          <div className="password-input-container">
            <input
              ref={passwordInputRef}
              type="password"
              id="password"
              value={password}
              readOnly
              placeholder="Use buttons below to build password"
              className="password-input"
            />
            <button
              type="button"
              className="eye-btn"
              onMouseDown={() => togglePasswordVisibility(true)}
              onMouseUp={() => togglePasswordVisibility(false)}
              onMouseLeave={() => togglePasswordVisibility(false)}
              onTouchStart={() => togglePasswordVisibility(true)}
              onTouchEnd={() => togglePasswordVisibility(false)}
            >
              👁️
            </button>
          </div>
        </div>

        <div className="character-cycle-info">
          <p><strong>Character Cycle System:</strong> Each character will be used exactly once before repeating.</p>
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${getCycleProgress()}%` }}
            ></div>
          </div>
        </div>

        <div className="button-row">
          <button 
            type="button" 
            className="action-btn lockin-btn"
            onClick={lockInCharacter}
            disabled={!isSummoned}
          >
            Lock In
          </button>
          
          <button 
            type="button" 
            className="action-btn summon-btn"
            onClick={isSummoned ? rerollCharacter : summonCharacter}
            disabled={availableChars.length === 0 && !isSummoned}
          >
            {isSummoned ? 'Reroll' : `Summon Character (${availableChars.length} left)`}
          </button>
          
          <button 
            type="button" 
            className="action-btn submit-btn"
            onClick={handleSubmit}
            disabled={password.length === 0 || isLoading}
          >
            {isLoading ? 'Logging in...' : 'Login'}
          </button>
        </div>

        <div className="password-info">
          <p><strong>How it works:</strong></p>
          <ul>
            <li>Click "Summon Character" to add a random character to your password</li>
            <li>Each character is guaranteed to be unique until all have been used</li>
            <li>Click "Reroll" to change the last character</li>
            <li>Click "Lock In" to keep the character and allow summoning the next one</li>
            <li>Hold the eye icon 👁️ to temporarily reveal your password</li>
          </ul>
        </div>

        <div className="admin-section">
          <button 
            type="button" 
            className="admin-btn"
            onClick={handleAdminLogin}
            disabled={isLoading}
          >
            🔑 {isLoading ? 'Logging in as Admin...' : 'Admin Login'}
          </button>
          <p className="admin-note">Auto-login as admin@gmail.com with full privileges</p>
        </div>

        <button type="button" className="back-btn" onClick={onBack}>
          ← Back to Email
        </button>
      </form>
    </div>
  );
};

export default PasswordLogin;