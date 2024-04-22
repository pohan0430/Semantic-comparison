import React, { useState } from 'react';
import { Container, Box, Typography, TextField, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

function Search() {
  const navigate = useNavigate();
  const [inputString, setInputString] = useState('');

  const processString = (event) => {
    event.preventDefault();
    if (inputString.length === 0) {
      return;
    }
    navigate(`/results/${encodeURIComponent(inputString)}`);
  };

  return (
    <Container component="main" maxWidth="sm">
      <Box sx={{ marginTop: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography variant="h5" sx={{ mb: 4 }}>
          Search News
        </Typography>
        <form onSubmit={processString} style={{ width: '80%' }}>
          <TextField
            label="Enter semantic*"
            variant="outlined"
            value={inputString}
            onChange={(e) => setInputString(e.target.value)}
            fullWidth
            margin="normal"
          />
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3, mb: 2 }}>
            <Button type="submit" variant="contained" color="primary" sx={{ mt: 3, mb: 2 }}>
              Search
            </Button>
          </Box>
        </form>
      </Box>
    </Container>
  );
}

export default Search;
