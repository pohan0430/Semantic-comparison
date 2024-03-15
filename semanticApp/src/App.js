import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import { AppBar, Toolbar, Button, Typography, Box, Container } from '@mui/material';
import Login from './Login';
import Script from './Script';
import Home from './Home';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
  };

  return (
    <Router>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Semantic App
            </Typography>
            {isLoggedIn && (
              <>
                <Button color="inherit" component={Link} to="/home">Home</Button>
                <Button color="inherit" component={Link} to="/search">Search</Button>
                <Button color="inherit" onClick={() => setIsLoggedIn(false)}>Logout</Button>
              </>
            )}
          </Toolbar>
        </AppBar>
        <Container component="main" maxWidth="xs">
          <Box sx={{ marginTop: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <Routes>
              <Route path="/login" element={!isLoggedIn ? <Login onLoginSuccess={handleLoginSuccess} /> : <Navigate replace to="/home" />} />
              <Route path="/home" element={isLoggedIn ? <Home /> : <Navigate replace to="/login" />} />
              <Route path="/search" element={isLoggedIn ? <Script /> : <Navigate replace to="/login" />} />
              <Route path="/" element={<Navigate replace to={isLoggedIn ? "/home" : "/login"} />} />
            </Routes>
          </Box>
        </Container>
      </Box>
    </Router>
  );
}

export default App;
