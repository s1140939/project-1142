// 基本的 JavaScript 互動功能
const greetButton = document.getElementById('greetButton');
const message = document.getElementById('message');

greetButton.addEventListener('click', () => {
  message.textContent = '你好！這是由 JavaScript 顯示的訊息。';
});
