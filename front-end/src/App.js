import React, { useState } from 'react';
import './App.css';
import Login from './components/Login';
 
function App() {
  const [user, setUser] = useState(null);

  return (
    <div className="App">
      {user ? (
        <header className="App-header">
          <h1>Welcome, {user.email} 🎉</h1>
          <p>You are now logged in to the demo app.</p>
          <button className="logout-btn" onClick={() => setUser(null)}>
            Logout
          </button>
        </header>
      ) : (
        <Login onLogin={setUser} />
      )}
    </div>
  );
}

export default App;
