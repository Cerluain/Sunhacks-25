import React, { useState } from 'react';
import EmailLogin from './EmailLogin';
import PasswordLogin from './PasswordLogin';
import SignUp from './SignUp';
import './Login.css';

const Login = ({ onLogin }) => {
  const [currentView, setCurrentView] = useState('email'); // 'email', 'password', 'signup'
  const [userEmail, setUserEmail] = useState('');

  const handleEmailSubmit = (email) => {
    setUserEmail(email);
    setCurrentView('password');
  };

  const handleBackToEmail = () => {
    setCurrentView('email');
  };

  const handleSwitchToSignUp = () => {
    setCurrentView('signup');
  };

  const handleSwitchToLogin = () => {
    setCurrentView('email');
  };

  const handleSignUp = (userData) => {
    onLogin(userData);
  };

  if (currentView === 'signup') {
    return <SignUp onSignUp={handleSignUp} onSwitchToLogin={handleSwitchToLogin} />;
  }

  if (currentView === 'password') {
    return (
      <PasswordLogin 
        email={userEmail}
        onLogin={onLogin}
        onBack={handleBackToEmail}
      />
    );
  }

  return (
    <EmailLogin 
      onEmailSubmit={handleEmailSubmit}
      onSwitchToSignUp={handleSwitchToSignUp}
    />
  );
};

export default Login;