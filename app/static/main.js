document.querySelector('form').addEventListener('submit', function() {
  let progressBar = document.querySelector('.progress-bar');
  progressBar.style.width = '0%';

  setInterval(function() {
    fetch('/progress')
      .then(response => response.json())
      .then(data => {
        progressBar.style.width = data.progress + '%';
        progressBar.innerHTML = data.progress + '%';
      });
  }, 1000);
});
