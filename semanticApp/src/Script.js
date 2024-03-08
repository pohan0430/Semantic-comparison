import React, { useState } from 'react';

function Script() {
  const [inputString, setInputString] = useState('');
  const [result, setResult] = useState('');

  const processString = () => {
    alert("Function called.");
    if (inputString.length === 0) {
        return;
    }

    fetch('http://127.0.0.1:5000/tags', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ tagname: inputString })
    })
    .then(response => response.json())
    .then(data => {
        setResult(JSON.stringify(data));
    })
      .catch(error => console.error('Error:', error));
  };


  return (
    <div>
      <label htmlFor="inputString">Enter semantic:</label>
      <input
        type="text"
        id="inputString"
        placeholder="Type a string"
        value={inputString}
        onChange={(e) => setInputString(e.target.value)}
      />
      <button onClick={processString}>Search</button>
      <pre>{result}</pre>
    </div>
  );
}

export default Script;
