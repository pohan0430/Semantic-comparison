import React, { useState, useEffect } from 'react';
import { Container, Typography, Card, CardContent, Checkbox, FormGroup, FormControlLabel, List, ListItem, Divider, Link, Button, Box, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';

function Results() {
  const [results, setResults] = useState([]);
  const [selectedNews, setSelectedNews] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const { inputString } = useParams();
  const navigate = useNavigate();
  const decodedInput = decodeURIComponent(inputString);

  useEffect(() => {
    fetch(`http://localhost:8008/search/${decodedInput}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      setResults(data.news);
    })
    .catch(error => console.error('error:', error));
  }, [decodedInput]);

  const handleOpenDialog = () => setOpenDialog(true);
  const handleCloseDialog = () => setOpenDialog(false);

  const handleSelectNews = (newsId, isChecked) => {
    setSelectedNews(prev => isChecked ? [...prev, newsId] : prev.filter(id => id !== newsId));
  };

  const handleCreateTag = () => {
    if (selectedNews.length === 0) {
        alert("At least choose one news。");
        return;
    }

    const tagName = encodeURIComponent(decodedInput.trim().replace(/ /g, '_'));

    const requestBody = { news_id: selectedNews };
    fetch(`http://localhost:8008/tag/${tagName}`, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        console.log("Error:", data.error);
        handleOpenDialog();
      } else {
        console.log("Tag created successfully:", data);
        setSelectedNews([]);
        navigate('/search');
      }
    })
    .catch(error => {
        console.error('Error creating tag:', error);
        alert("An error occurred while creating the tag.");
    });
  };

  const handleUpdateTag = () => {
    if (selectedNews.length === 0) {
      alert("At least choose one news。");
      return;
    }

    const tagName = encodeURIComponent(decodedInput.trim().replace(/ /g, '_'));
    const requestBody = { news_id: selectedNews };

    fetch(`http://localhost:8008/tag/${tagName}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        alert("Error updating tag: " + data.error);
      } else {
        console.log("Tag updated successfully:", data);
        setSelectedNews([]);
        navigate('/search');
      }
    })
    .catch(error => {
      console.error('Error updating tag:', error);
      alert("An error occurred while updating the tag.");
    });
  };

  return (
    <Container component="main" sx={{ maxWidth: '1200px', width: '100%', display: 'flex', 
  flexDirection: 'column',  alignItems: 'center' }}>
      <Typography variant="h4" sx={{ mt: 2, mb: 2 }}>
        Searching results
      </Typography>
      <List sx={{ width: '250%', maxWidth: 1000, margin: 'left' }}>
        {results.map((item, index) => (
          <ListItem key={item.news_id} sx={{ display: 'flex', flexDirection: 'column', alignItems: 'auto', width: '100%' }}>
            <Card variant="outlined" sx={{ width: '250%', maxWidth: 600, margin: 'auto', mb: 4 }}>
              <FormGroup sx={{ position: 'absolute', top: 0, left: 100 }}>
                <FormControlLabel
                  control={<Checkbox checked={selectedNews.includes(item.news_id)} onChange={(e) => handleSelectNews(item.news_id, e.target.checked)} />}
                  label=""
                />
              </FormGroup>
              <CardContent>
                <Typography variant="h5">{item.title}</Typography>
                <Typography color="text.secondary" sx={{ mb: 1.5 }}>
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
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2, mb: 4 }}>
        <Button onClick={handleCreateTag} variant="contained" color="primary">
          Create Tag
        </Button>
      </Box>
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>{"Tag already exists."}</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Tag already exists.Sure to update this tag？
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog} color="secondary" autoFocus>
            Cancel
          </Button>
          <Button onClick={handleUpdateTag} color="primary">
            Update
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default Results;
