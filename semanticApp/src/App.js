import './App.css';
import React, { useState } from 'react';
import Login from './Login';
import Script from './Script';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
  };

  return (
    <div className="App">
      <header className="App-header">
        {!isLoggedIn ? (
          <Login onLoginSuccess={handleLoginSuccess} />
        ) : (
          <Script />
        )}
      </header>
    </div>
  );
}

export default App;
