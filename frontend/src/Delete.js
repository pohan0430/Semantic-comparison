import React, { useState } from 'react';
import {
  Container, Box, Typography, TextField, Button, Modal, IconButton
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

function Delete() {
  const [tagName, setTagName] = useState('');
  const [open, setOpen] = useState(false);
  const [status, setStatus] = useState('');

  const handleClose = () => {
    setOpen(false);
    setStatus('');
  };

  const handleDelete = (event) => {
    event.preventDefault();
    if (tagName.trim().length === 0) {
      alert("Please enter a tag name.");
      return;
    }

    fetch(`http://localhost:8008/tag/${encodeURIComponent(tagName)}`, {
      method: 'DELETE',
    })
      .then(response => {
        if (response.ok) {
          setStatus('Success: Tag deleted successfully');
          setTagName('');
        } else {
          throw new Error('Failed to delete the tag');
        }
      })
      .then(data => {
        setTagName('');
      })
      .catch(error => {
        console.error(`Error fetching news for tag ${tagName}:`, error);
      });
    setOpen(true);
  };

  const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box sx={{ marginTop: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography variant="h5" sx={{ mb: 4 }}>
          Delete Tag
        </Typography>
        <form onSubmit={handleDelete} style={{ width: '100%' }}>
          <TextField
            label="Enter Tag Name*"
            variant="outlined"
            value={tagName}
            onChange={(e) => setTagName(e.target.value)}
            fullWidth
            margin="normal"
          />
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3, mb: 2 }}>
            <Button type="submit" variant="contained" color="primary">
              Delete Tag
            </Button>
          </Box>
        </form>
        <Modal open={open} onClose={handleClose}>
          <Box sx={style}>
            <IconButton onClick={handleClose} sx={{ position: 'absolute', right: 8, top: 8 }}>
              <CloseIcon />
            </IconButton>
            <Typography variant="h6" component="h2">
              {status}
            </Typography>
          </Box>
        </Modal>
      </Box>
    </Container>
  );
}

export default Delete;
