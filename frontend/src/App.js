import React, { useState } from 'react';
import { Routes, Route, Link, Navigate, useNavigate  } from 'react-router-dom';
import { AppBar, Toolbar, Button, Typography, Box, Container, Menu, MenuItem  } from '@mui/material';
import Login from './Login';
import Search from './Search';
import Results from './Results';
import Delete from './Delete';
import { History, TagDetails } from './History';
import Home from './Home';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);
  const navigate = useNavigate();

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleNavigate = (path) => {
    navigate(path);
    handleClose();
  };

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
  };

  const NotFound = () => {
    const navigate = useNavigate();

    return (
      <Container component="main" maxWidth="lg" sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography variant="h4" gutterBottom>
          404 Not Found
        </Typography>
        <Typography variant="subtitle1">
          Sorry, the page you are looking for does not exist.
        </Typography>
        <Button variant="contained" color="primary" sx={{ mt: 3 }} onClick={() => navigate('/')}>
          Go Home
        </Button>
      </Container>
    );
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Semantic App
          </Typography>
          {isLoggedIn && (
            <>
              <Button color="inherit" component={Link} to="/home">Home</Button>
              <Button color="inherit" aria-controls="menu-appbar" aria-haspopup="true" onClick={handleMenu}>
                Options
              </Button>
              <Menu
                id="menu-appbar"
                anchorEl={anchorEl}
                anchorOrigin={{
                  vertical: 'bottom',
                  horizontal: 'right',
                }}
                transformOrigin={{
                  vertical: 'top',
                  horizontal: 'right',
                }}
                open={open}
                onClose={handleClose}
                sx={{
                  "& .MuiPaper-root": {
                    backgroundColor: "primary.main",
                    color: "white",
                    boxShadow: "0px 4px 20px rgba(0,0,0,0.5)",
                  }
                }}
              >
                <MenuItem onClick={() => handleNavigate('/search')} sx={{ '&:hover': { backgroundColor: "primary.light", color: "black" } }}>Search</MenuItem>
                <MenuItem onClick={() => handleNavigate('/delete')} sx={{ '&:hover': { backgroundColor: "primary.light", color: "black" } }}>Delete</MenuItem>
                <MenuItem onClick={() => handleNavigate('/history')} sx={{ '&:hover': { backgroundColor: "primary.light", color: "black" } }}>History</MenuItem>
              </Menu>
              <Button color="inherit" onClick={() => setIsLoggedIn(false)}>Logout</Button>
            </>
          )}
        </Toolbar>
      </AppBar>
      <Container component="main" maxWidth="lg">
        <Box sx={{ marginTop: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <Routes>
            <Route path="/login" element={!isLoggedIn ? <Login onLoginSuccess={handleLoginSuccess} /> : <Navigate replace to="/home" />} />
            <Route path="/home" element={isLoggedIn ? <Home /> : <Navigate replace to="/login" />} />
            <Route path="/search/*" element={isLoggedIn ? <Search /> : <Navigate replace to="/login" />} />
            <Route path="/delete/*" element={isLoggedIn ? <Delete /> : <Navigate replace to="/login" />} />
            <Route path="/results/:inputString" element={<Results />} />
            <Route path="/history/*" element={isLoggedIn ? <History /> : <Navigate replace to="/login" />} />
            <Route path="/tags/:tagname" element={<TagDetails />} />
            <Route path="/" element={<Navigate replace to={isLoggedIn ? "/home" : "/login"} />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Box>
      </Container>
    </Box>
  );
}

export default App;
