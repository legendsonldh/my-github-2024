var messages = [
  "A large number of users in the queue<br>Request will be processed within 10 minutes<br>Why not give the project a Star while waiting!",
  "目前有大量用户排队<br>您的请求将在提交后的 10 分钟内处理<br>不如在等待时给项目点个 Star 吧！",
];
var messageIndex = 0;

// Function to change the loading text
function changeLoadingText() {
  document.querySelector('.loading-text').innerHTML = messages[messageIndex];
  messageIndex = (messageIndex + 1) % messages.length;
}

// Change the loading text every 6 seconds
setInterval(changeLoadingText, 6000);