import React, { useState } from 'react';
import './SignUp.css';
import { authAPI, handleAPIError } from '../services/api';

const SignUp = ({ onSignUp, onSwitchToLogin }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const passwordRequirements = {
    hasUpperCase: /[A-Z]/.test(formData.password),
    hasLowerCase: /[a-z]/.test(formData.password),
    hasNumber: /[0-9]/.test(formData.password),
    hasSpecialChar: /[-_.!@#$%&*+.+]/.test(formData.password),
    hasMinLength: formData.password.length >= 8
  };

  const validateForm = () => {
    const newErrors = {};

    // Email validation
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else {
      if (!passwordRequirements.hasUpperCase) newErrors.password = 'Missing uppercase letter';
      if (!passwordRequirements.hasLowerCase) newErrors.password = 'Missing lowercase letter';
      if (!passwordRequirements.hasNumber) newErrors.password = 'Missing number';
      if (!passwordRequirements.hasSpecialChar) newErrors.password = 'Missing special character';
      if (!passwordRequirements.hasMinLength) newErrors.password = 'Must be at least 8 characters';
    }

    // Confirm password validation
    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      setIsLoading(true);
      setErrors({});
      
      try {
        // Register user with backend API
        const response = await authAPI.register(formData.email, formData.password);
        
        // Auto-login after successful registration
        await authAPI.login(formData.email, formData.password);
        
        // Call parent component with user data
        onSignUp({ 
          email: formData.email,
          id: response.id,
          message: response.message
        });
      } catch (error) {
        const errorMessage = handleAPIError(error);
        setErrors({ submit: errorMessage });
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const allRequirementsMet = Object.values(passwordRequirements).every(requirement => requirement);

  return (
    <div className="signup-container">
      <form className="signup-form" onSubmit={handleSubmit}>
        <h2>Create Your Account</h2>
        
        <div className="form-group">
          <label htmlFor="email">
            Email Address <span className="required">*</span>
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="Enter your email"
            className={errors.email ? 'error' : ''}
          />
          {errors.email && <span className="error-message">{errors.email}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="password">
            Password <span className="required">*</span>
          </label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Create a password"
            className={errors.password ? 'error' : ''}
          />
          {errors.password && <span className="error-message">{errors.password}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="confirmPassword">
            Confirm Password <span className="required">*</span>
          </label>
          <input
            type="password"
            id="confirmPassword"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleChange}
            placeholder="Confirm your password"
            className={errors.confirmPassword ? 'error' : ''}
          />
          {errors.confirmPassword && <span className="error-message">{errors.confirmPassword}</span>}
        </div>

        {/* Password Requirements */}
        <div className="password-requirements">
          <h4>Password Requirements:</h4>
          <ul>
            <li className={passwordRequirements.hasUpperCase ? 'met' : 'unmet'}>
              ✓ At least 1 uppercase letter
            </li>
            <li className={passwordRequirements.hasLowerCase ? 'met' : 'unmet'}>
              ✓ At least 1 lowercase letter
            </li>
            <li className={passwordRequirements.hasNumber ? 'met' : 'unmet'}>
              ✓ At least 1 number
            </li>
            <li className={passwordRequirements.hasSpecialChar ? 'met' : 'unmet'}>
              ✓ At least 1 special character (-, _, ., !, @, #, $, %, &, *, +)
            </li>
            <li className={passwordRequirements.hasMinLength ? 'met' : 'unmet'}>
              ✓ At least 8 characters long
            </li>
          </ul>
        </div>

        {errors.submit && <div className="error-message submit-error">{errors.submit}</div>}

        <button 
          type="submit" 
          className={`signup-btn ${allRequirementsMet && !isLoading ? 'active' : ''}`}
          disabled={!allRequirementsMet || !formData.confirmPassword || isLoading}
        >
          {isLoading ? 'Creating Account...' : 'Sign Up'}
        </button>

        <div className="switch-form">
          <p>Already have an account?</p>
          <button type="button" className="switch-btn" onClick={onSwitchToLogin}>
            Login here
          </button>
        </div>
      </form>
    </div>
  );
};

export default SignUp;