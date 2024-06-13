import React from 'react';
import { Typography, Container, Box } from '@mui/material';

function Home() {
  return (
    <Container maxWidth="md" sx={{ mt: 8, overflow: 'hidden' }}>
      <Box sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: 200,
        mb: 4
      }}>
        <img src={`${process.env.PUBLIC_URL + '/home.png'}`} alt="Home" style={{ width: '100%', height: 'auto', maxHeight: '100%' }} />
      </Box>
      <Typography variant="h4" sx={{ fontWeight: 'bold', mb: 2, textAlign: 'center' }}>
        歡迎使用標籤搜尋
      </Typography>
      <Typography variant="body1" sx={{ textAlign: 'center' }}>
        搜尋您有興趣的語意.
      </Typography>
    </Container>
  );
}

export default Home;
