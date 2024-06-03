import React, { useState } from 'react';
import { Box, TextField, Button } from '@mui/material';

function Login({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    onLoginSuccess({ username, password });
  };

  return (
    <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1, width: '30%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <TextField
        margin="normal"
        required
        fullWidth
        id="username"
        label="User name"
        name="username"
        autoComplete="username"
        autoFocus
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <TextField
        margin="normal"
        required
        fullWidth
        name="password"
        label="Password"
        type="password"
        id="password"
        autoComplete="current-password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <Box sx={{ width: '100%', display: 'flex', justifyContent: 'center', mt: 3, mb: 2 }}>
        <Button
          type="submit"
          variant="contained"
        >
          Sign In
        </Button>
      </Box>
    </Box>
  );
}

export default Login;
