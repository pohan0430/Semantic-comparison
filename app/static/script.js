function processString() {
    console.log("Function called.");
    var inputString = document.getElementById('inputString').value;

    if (inputString.length == 0) {
        return;
    }

    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input_string: inputString })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').textContent = JSON.stringify(data);
    })
    .catch(error => console.error('Error:', error));
}
