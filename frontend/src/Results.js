import React, { useState, useEffect, useCallback } from 'react';
import { Container, TextField, Typography, Card, CardMedia, CardContent, Checkbox, FormGroup, FormControlLabel, List, ListItem, Divider, Link, Button, Box, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle , CircularProgress } from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';

function Results() {
  const [results, setResults] = useState([]);
  const [selectedNews, setSelectedNews] = useState([]);
  const [totalAudience, setTotalAudience] = useState(0);
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [newsPerPage] = useState(10);
  const [topNRank, setTopNRank] = useState(20);
  const [openDialog, setOpenDialog] = useState(false);
  const [openSuccessDialog, setOpenSuccessDialog] = useState(false);
  const [updateSuccessDialog, setUpdateSuccessDialog] = useState(false);
  const { inputString } = useParams();
  const navigate = useNavigate();
  const decodedInput = decodeURIComponent(inputString);

  const fetchNews = useCallback(() => {
    fetch(`http://localhost:8008/search/${decodedInput}?top_n_rank=${topNRank}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      console.log("Fetched data:", data);
      setResults(data.news);
    })
    .catch(error => console.error('error:', error));
  }, [decodedInput, topNRank]);

  useEffect(() => {
    fetchNews();
  }, [fetchNews]);

  const handleOpenDialog = () => setOpenDialog(true);
  const handleCloseDialog = () => setOpenDialog(false);

  const handleOpenSuccessDialog = () => {
    setOpenSuccessDialog(true);
    setTimeout(() => {
      setOpenSuccessDialog(false);
      navigate('/history');
    }, 2000);
  };

  const handleCloseSuccessDialog = () => {
    setOpenSuccessDialog(false);
    navigate('/history');
  };

  const handleOpenUpdateDialog = () => {
    setUpdateSuccessDialog(true);
    setTimeout(() => {
      setUpdateSuccessDialog(false);
      navigate('/history');
    }, 2000);
  };

  const handleCloseUpdateDialog = () => {
    setUpdateSuccessDialog(false);
    navigate('/history');
  };

  const indexOfLastNews = currentPage * newsPerPage;
  const indexOfFirstNews = indexOfLastNews - newsPerPage;
  const currentNews = results.slice(indexOfFirstNews, indexOfLastNews);

  const totalPage = Math.ceil(results.length / newsPerPage);

  const handlePrevPage = () => {
    setCurrentPage(prev => prev > 1 ? prev - 1 : prev);
  };

  const handleNextPage = () => {
    setCurrentPage(prev => prev < Math.ceil(results.length / newsPerPage) ? prev + 1 : prev);
  };

  const handleChangeTopNRank = (event) => {
    setTopNRank(event.target.value);
  };

  const handleSetTopNRank = async () => {
    console.log("Sending request to /total_audience with news_ids:", selectedNews);
    setLoading(true);

    fetch("http://localhost:8008/total_audience", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ news_ids: selectedNews }),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log("Response from /total_audience:", data);
      if (Array.isArray(data) && data.length > 0) {
        setTotalAudience(data[0].unique_audience);
      } else {
        setTotalAudience(0);
      }
    })
    .catch(error => {
      console.error("Request failed:", error);
    })
    .finally(() => {
      setLoading(false);
    });
  };

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
        handleOpenSuccessDialog();
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
        handleOpenUpdateDialog();
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
        搜尋結果
      </Typography>
      <Typography variant="h5" sx={{ mt: 2, mb: 2 }}>
        總預估人數: {totalAudience}
      </Typography>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <TextField
          label="Number of News Items"
          type="number"
          variant="outlined"
          value={topNRank}
          onChange={handleChangeTopNRank}
          sx={{ mr: 2, width: 150 }}
        />
        <Button variant="contained" color="primary" onClick={handleSetTopNRank}>
          設定
        </Button>
        {loading && <CircularProgress sx={{ ml: 2 }} />}
      </Box>
      <List sx={{ width: '250%', maxWidth: 1000, margin: 'left' }}>
          {currentNews.map((item, index) => (
              <ListItem key={item.news_id} sx={{ display: 'flex', flexDirection: 'column', alignItems: 'auto', width: '100%' }}>
                  <Card variant="outlined" sx={{ display: 'flex', flexDirection: 'row-reverse', justifyContent: 'space-between', width: '250%', maxWidth: 600, margin: 'auto', mb: 4 }}>
                      <CardMedia
                          component="img"
                          sx={{ width: 160, maxHeight: 200, objectFit: 'cover' }}
                          image={item.img}
                          alt={`Image for ${item.title}`}
                      />
                      <Box sx={{ display: 'flex', flexDirection: 'column', flexGrow: 1 }}>
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
                                  Audiences: {item.audience}
                                  <br />
                                  <Link href={item.url} target="_blank">Read more</Link>
                              </Typography>
                          </CardContent>
                      </Box>
                  </Card>
                  {index < currentNews.length - 1 && <Divider />}
              </ListItem>
          ))}
      </List>
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2, mb: 4 }}>
        <Button 
          onClick={handlePrevPage} 
          variant="contained" 
          color="primary"
          sx={{ minWidth: 120, height: 36, mr: 2 }}
        >
          前一頁
        </Button>
        <Typography sx={{ alignSelf: 'center' }}>
          Page {currentPage} of {totalPage}
        </Typography>
        <Button 
          onClick={handleNextPage} 
          variant="contained" 
          color="primary"
          sx={{ minWidth: 120, height: 36, mx: 2 }}
        >
          下一頁
        </Button>
        <Button 
          onClick={handleCreateTag} 
          variant="contained" 
          color="primary" 
          sx={{ minWidth: 120, height: 36 }}
        >
          創建標籤
        </Button>
      </Box>
      <Dialog open={openDialog} onClose={handleCloseDialog}>
        <DialogTitle>{"Tag already exists."}</DialogTitle>
        <DialogContent>
          <DialogContentText>
            標籤已經存在. 確定要更新此標籤？
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog} color="secondary" autoFocus>
            取消
          </Button>
          <Button onClick={handleUpdateTag} color="primary">
            更新
          </Button>
        </DialogActions>
      </Dialog>
      <Dialog open={openSuccessDialog} onClose={handleCloseSuccessDialog}>
        <DialogTitle>{"Tag Created Successfully"}</DialogTitle>
        <DialogContent>
          <DialogContentText>
            標籤創建成功.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseSuccessDialog} color="primary">
            確定
          </Button>
        </DialogActions>
      </Dialog>
      <Dialog open={updateSuccessDialog} onClose={handleCloseUpdateDialog}>
        <DialogTitle>{"Tag Updated Successfully"}</DialogTitle>
        <DialogContent>
          <DialogContentText>
            標籤更新成功.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseUpdateDialog} color="primary">
            確定
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default Results;
