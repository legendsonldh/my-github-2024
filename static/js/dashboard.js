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
        "数据加载中，请坐和放宽",
        "Chargement des données, veuillez vous asseoir et vous détendre",
        "Cargando datos, por favor siéntese y relájese",
        "データを読み込んでいます、座ってリラックスしてください",
        "데이터를로드 중입니다. 앉아서 편안하게하세요",
        "Загрузка данных, пожалуйста, сядьте и расслабьтесь",
    ];
    var messageIndex = 0;

    // Function to change the loading text
    function changeLoadingText() {
        document.querySelector('.loading-text').textContent = messages[messageIndex];
        messageIndex = (messageIndex + 1) % messages.length;
    }

    // Change the loading text every 1.5 seconds
    setInterval(changeLoadingText, 1500);

    // Create an AbortController to handle the timeout
    const controller = new AbortController();
    const signal = controller.signal;

    // Set a very long timeout (e.g., 1 hour)
    const timeoutId = setTimeout(() => controller.abort(), 3600000);

    fetch("/load", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            access_token: accessToken,
            username: username,
            timezone: timezone,
            year: year
        }),
        signal: signal
    })
        .then(response => response.json())
        .then(data => {
            clearTimeout(timeoutId); // Clear the timeout if the request completes successfully
            window.location.href = data.redirect_url;
        })
        .catch(error => {
            if (error.name === 'AbortError') {
                console.error('Fetch aborted due to timeout');
            } else {
                console.error('Error:', error);
            }
            document.querySelector('.loader').style.display = 'none';
            messages = [
                "An error occurred while loading data, check your python console for more information",
            ];
        });
});