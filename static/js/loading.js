document.getElementById('inputForm').addEventListener('submit', function (event) {
    var accessToken = document.getElementById('accessToken').value;
    if (!accessToken.startsWith('ghp_')) {
        event.preventDefault();
        alert('Access Token must start with "ghp_"');
    }
});

document.getElementById('inputForm').addEventListener('submit', function (event) {
    event.preventDefault();
    var accessToken = document.getElementById('accessToken').value;
    var username = document.getElementById('username').value;
    var timezone = document.getElementById('timezone').value;
    var year = document.getElementById('year').value;

    // Hide the form
    document.getElementById('inputForm').style.display = 'none';
    // Show the loader and loading text
    document.querySelector('.loader').style.display = 'block';
    document.querySelector('.loading-text').style.display = 'block';

    // Messages to display
    var messages = [
        "Loading data, please sit down and relax",
        "数据加载中，请坐和放宽"
    ];
    var messageIndex = 0;

    // Function to change the loading text
    function changeLoadingText() {
        document.querySelector('.loading-text').textContent = messages[messageIndex];
        messageIndex = (messageIndex + 1) % messages.length;
    }

    // Change the loading text every 3 seconds
    setInterval(changeLoadingText, 3000);

    fetch("/load_data", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            access_token: accessToken,
            username: username,
            timezone: timezone,
            year: year
        })
    })
        .then(response => response.json())
        .then(data => {
            window.location.href = data.redirect_url;
        })
        .catch(error => {
            document.querySelector('.loader').style.display = 'none';
            messages = [
                "An error occurred while loading data, check your python console for more information",
            ];
            console.error('Error:', error);
        });
});