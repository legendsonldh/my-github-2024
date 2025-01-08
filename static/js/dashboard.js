document.getElementById('inputForm').addEventListener('submit', function (event) {
  event.preventDefault();
  var accessToken = document.getElementById('accessToken').value;
  var username = document.getElementById('username').value;
  var timezone = document.getElementById('timezone').value;
  var year = document.getElementById('year').value;

  // Hide the form
  document.getElementById('inputForm').style.display = 'none';

  console.log("fetch data from gitlab")

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
  })
    .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('Error occurred while loading data.');
      }
    })
    .then(data => {
      if (data.redirect_url) {
        window.location.href = data.redirect_url;
      } else {
        throw new Error('Invalid response from server.');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      document.querySelector('.loader').style.display = 'none';
      alert("An error occurred while loading data.");
    });
});