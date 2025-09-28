/**
 * Centralized API service for handling all backend communications
 */

// Base URL for API calls - will work for both development and production
const API_BASE_URL = '/api';

/**
 * Helper function to handle API responses
 */
const handleResponse = async (response) => {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }
  return response.json();
};

/**
 * Helper function to get auth headers
 */
const getAuthHeaders = () => {
  const token = localStorage.getItem('authToken');
  return token ? { 'Authorization': `Bearer ${token}` } : {};
};

/**
 * Authentication API calls
 */
export const authAPI = {
  /**
   * Register a new user
   * @param {string} email - User's email
   * @param {string} password - User's password
   * @returns {Promise<Object>} User data
   */
  register: async (email, password) => {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });
    return handleResponse(response);
  },

  /**
   * Login user
   * @param {string} email - User's email (used as username)
   * @param {string} password - User's password
   * @returns {Promise<Object>} Token data
   */
  login: async (email, password) => {
    // FastAPI OAuth2PasswordRequestForm expects form data
    const formData = new FormData();
    formData.append('username', email); // Backend uses email as username
    formData.append('password', password);

    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      body: formData,
    });
    
    const data = await handleResponse(response);
    
    // Store token in localStorage for future requests
    if (data.access_token) {
      localStorage.setItem('authToken', data.access_token);
    }
    
    return data;
  },

  /**
   * Logout user (clear local token and notify backend)
   */
  logout: async () => {
    const token = localStorage.getItem('authToken');
    
    // Always clear local token first
    localStorage.removeItem('authToken');
    
    // If we have a token, notify the backend to blacklist it
    if (token) {
      try {
        await fetch(`${API_BASE_URL}/auth/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
      } catch (error) {
        // Even if backend logout fails, we've already cleared the local token
        console.warn('Backend logout failed, but local token was cleared:', error);
      }
    }
  },

  /**
   * Check if user is currently logged in
   * @returns {boolean} Whether user has a valid token
   */
  isLoggedIn: () => {
    const token = localStorage.getItem('authToken');
    if (!token) return false;
    
    try {
      // Check if token is expired (basic check)
      const payload = JSON.parse(atob(token.split('.')[1]));
      const now = Date.now() / 1000;
      return payload.exp > now;
    } catch (error) {
      // If token is invalid, remove it
      localStorage.removeItem('authToken');
      return false;
    }
  },

  /**
   * Admin login (automatic login with admin credentials)
   * @returns {Promise<Object>} Token data
   */
  adminLogin: async () => {
    const response = await fetch(`${API_BASE_URL}/auth/admin-login`, {
      method: 'POST',
    });
    
    const data = await handleResponse(response);
    
    // Store token in localStorage for future requests
    if (data.access_token) {
      localStorage.setItem('authToken', data.access_token);
    }
    
    return data;
  },
  /**
   * Get current user info from token
   * @returns {Object|null} User info or null if not logged in
   */
  getCurrentUser: () => {
    const token = localStorage.getItem('authToken');
    if (!token) return null;
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return {
        email: payload.sub,
        user_id: payload.user_id,
        is_admin: payload.is_admin || false,
        exp: payload.exp
      };
    } catch (error) {
      return null;
    }
  },

  /**
   * Get current user info from backend (authenticated call)
   * @returns {Promise<Object>} User info from backend
   */
  getUserInfo: async () => {
    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      method: 'GET',
      headers: {
        ...getAuthHeaders(),
      },
    });
    return handleResponse(response);
  }
};

/**
 * Chat API calls
 */
export const chatAPI = {
  /**
   * Send a question to the AI chatbot
   * @param {string} question - The question to ask
   * @param {boolean} includeHistory - Whether to include conversation history
   * @returns {Promise<Object>} Chat response
   */
  askQuestion: async (question, includeHistory = true) => {
    const response = await fetch(`${API_BASE_URL}/chat/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
      body: JSON.stringify({
        question,
        include_history: includeHistory,
      }),
    });
    return handleResponse(response);
  }
};

/**
 * Generic API error handler for components
 */
export const handleAPIError = (error) => {
  console.error('API Error:', error);
  
  if (error.message.includes('401') || error.message.includes('unauthorized')) {
    // Token might be expired, clear it and redirect to login
    authAPI.logout();
    return 'Your session has expired. Please log in again.';
  }
  
  if (error.message.includes('409') || error.message.includes('conflict')) {
    return 'This email is already registered. Please use a different email or try logging in.';
  }
  
  if (error.message.includes('422')) {
    return 'Invalid input data. Please check your information and try again.';
  }
  
  return error.message || 'An unexpected error occurred. Please try again.';
};

const apiService = { authAPI, chatAPI, handleAPIError };
export default apiService;