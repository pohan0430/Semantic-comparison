import React, { useState, useEffect } from 'react';
import { useParams, Link as RouterLink, useNavigate } from 'react-router-dom';
import { Paper, Container, Button, List, ListItem, ListItemText, Typography, Card, CardContent, CardActions, Link } from '@mui/material';
function History() {
  const [tags, setTags] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:8008/tags`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => setTags(data.tags))
      .catch(error => console.error('Error fetching tags:', error));
  }, []);

  return (
    <Container component="main" maxWidth="xs" sx={{ maxWidth: '1200px', width: '100%', display: 'flex', flexDirection: 'column', mt: 4 }}>
    <Paper elevation={4} sx={{ p: 2, backgroundColor: '#f7f7f7', borderRadius: '10px' }}>
      <Typography variant="h4" sx={{ color: '#3f51b5', mb: 3 }}>
        Tag History
      </Typography>
      <List>
        {tags.map((tagId) => (
          <ListItem 
            key={tagId} 
            component={RouterLink} 
            to={`/tags/${tagId}`}
            sx={{ 
              mb: 1, 
              borderRadius: '5px', 
              '&:hover': { 
                backgroundColor: '#e3f2fd'
              }
            }}>
            <ListItemText primary={`Tag ${tagId}`} sx={{ color: '#333' }} />
          </ListItem>
        ))}
      </List>
    </Paper>
  </Container>
  );
}

function TagDetails() {
  const { tagname } = useParams();
  const navigate = useNavigate();
  const [news, setNews] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:8008/tag/${tagname}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP status ${response.status}`);
        }
        return response.json();
        })
      .then(data => setNews(data.news))
      .catch(error => console.error(`Error fetching news for tag ${tagname}:`, error));
  }, [tagname]);

  const handleBack = () => {
    navigate(-1);
  };

  return (
    <Container component="main" sx={{ maxWidth: '1000px', width: '100%', display: 'flex', 
  flexDirection: 'column',  alignItems: 'auto' }}>
      <Typography variant="h4" sx={{ mt: 2, mb: 2, fontWeight: 'bold' }}>
        News for Tag: {tagname}
      </Typography>
      <Button onClick={handleBack}  variant="contained" color="primary" sx={{width: '10%', mt: 2, mb: 2 }}>Back</Button>
      {news.map((item, index) => (
        <Card key={index} sx={{ width: '100%', maxWidth: 1280, mb: 2, boxShadow: 3 }}>
          <CardContent>
            <Typography variant="h6" sx={{ fontWeight: 'medium' }}>
              {item.title}
            </Typography>
            <Typography color="text.secondary" sx={{ mb: 1.5 }}>
              {item.cat_lv1} / {item.cat_lv2} - {item.date}
            </Typography>
            <Typography variant="body1" sx={{ mb: 1 }}>
              {Array.isArray(item.keywords) ? item.keywords.join(', ') : item.keywords}
            </Typography>
          </CardContent>
          <CardActions>
            <Button size="small" variant="outlined" color="primary">
              <Link href={item.url} target="_blank" rel="noopener noreferrer" underline="none">
                Read More
              </Link>
            </Button>
          </CardActions>
        </Card>
      ))}
    </Container>
  );
}

export { History, TagDetails };
