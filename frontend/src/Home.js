import React from 'react';
import { Box, Typography } from '@mui/material';

function Home() {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mt: 8 }}>
      <Typography variant="h4" sx={{ whiteSpace: 'nowrap' }}>
        Welcome to the Semantic App
      </Typography>
      <Typography variant="body1" sx={{ mt: 2 }}>
        Search the news you are interested in.
      </Typography>
    </Box>
  );
}

export default Home;
