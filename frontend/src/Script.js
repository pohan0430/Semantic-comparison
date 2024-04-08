import React, { useState } from 'react';
import { Container, Modal, Box, Typography, Link, List, ListItem, Divider, TextField, Button, Card, CardContent, IconButton, Checkbox, FormGroup, FormControlLabel } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

function Script() {
  const [inputString, setInputString] = useState('');
  const [results, setResults] = useState([]);
  const [selectedNews, setSelectedNews] = useState([]);
  const [open, setOpen] = useState(false);

  const processString = (event) => {
    event.preventDefault();
    if (inputString.length === 0) {
      return;
    }

    fetch(`http://localhost:8008/search/${encodeURIComponent(inputString)}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => {
        setResults(data.news);
      })
      .catch(error => console.error('Error:', error));
    setOpen(true);
  };

  const handleClose = () => setOpen(false);

  const handleSelectNews = (event, newsId) => {
    setSelectedNews(prev => {
      if (event.target.checked) {
        return [...prev, newsId];
      } else {
        return prev.filter(id => id !== newsId);
      }
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (inputString.trim().length === 0 || selectedNews.length === 0) {
      alert("Please enter a tag name and select at least one news.");
      return;
    }

    fetch(`http://localhost:8008/tag/${encodeURIComponent(inputString)}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ news_id: selectedNews })
    })
      .then(response => response.json())
      .then(data => {
        console.log('Success:', data);
        setOpen(false);
        setSelectedNews([]);
      })
      .catch(error => console.error('Error:', error));
  };

  const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 'auto',
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
    overflow: 'auto',
    maxHeight: '80%',
  };

  return (
    <Container component="main" maxWidth="sm">
      <Box sx={{ marginTop: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <form onSubmit={processString} style={{ width: '100%' }}>
          <TextField
            label="Enter semantic*"
            variant="outlined"
            value={inputString}
            onChange={(e) => setInputString(e.target.value)}
            fullWidth
            margin="normal"
            sx={{
              bgcolor: '#fff',
              input: { color: '#000' },
              '& .MuiOutlinedInput-root': {
                '& fieldset': {
                  borderColor: '#000',
                },
                '&:hover fieldset': {
                  borderColor: 'primary.light',
                },
                '&.Mui-focused fieldset': {
                  borderColor: 'primary.light',
                },
              },
              '& .MuiInputLabel-root': {
                color: '#000',
                '&.Mui-focused': {
                  color: 'primary.light',
                },
              }
            }}
          />
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3, mb: 2 }}>
            <Button type="submit" variant="contained" color="primary" sx={{ mt: 3, mb: 2 }}>
              Search
            </Button>
          </Box>
        </form>
        <Modal open={open} onClose={handleClose}>
          <Box sx={style}>
            <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
              <IconButton onClick={handleClose}>
                <CloseIcon />
              </IconButton>
            </Box>
            <Typography variant="h6" component="h2" sx={{ mb: 2 }}>
              Searching Results...
            </Typography>
            <form onSubmit={handleSubmit}>
              <List>
                {results.map((item, index) => (
                  <ListItem key={item.news_id} sx={{ flexDirection: 'column', alignItems: 'flex-start' }}>
                    <FormGroup>
                      <FormControlLabel control={<Checkbox onChange={(e) => handleSelectNews(e, item.news_id)} />} label="Select" />
                    </FormGroup>
                    <Card variant="outlined" sx={{ width: '100%', mb: 2 }}>
                      <CardContent>
                        <Typography variant="h5" component="div">
                          {item.title}
                        </Typography>
                        <Typography sx={{ mb: 1.5 }} color="text.secondary">
                          Category: {item.cat_lv1} / {item.cat_lv2}
                        </Typography>
                        <Typography variant="body2">
                          Keywords: {item.keywords}
                          <br />
                          <Link href={item.url} target="_blank">Read more</Link>
                        </Typography>
                      </CardContent>
                    </Card>
                    {index < results.length - 1 && <Divider />}
                  </ListItem>
                ))}
              </List>
              <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3, mb: 2 }}>
                <Button type="submit" variant="contained" color="primary">
                  Create Tag
                </Button>
              </Box>
            </form>
          </Box>
        </Modal>
      </Box>
    </Container>
  );
}

export default Script;
