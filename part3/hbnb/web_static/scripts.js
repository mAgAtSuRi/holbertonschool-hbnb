document.addEventListener('DOMContentLoaded', () => {
  // --- Header ---
  fetch("header.html")
    .then(response => response.text())
    .then(data => {
      document.getElementById("header-container").innerHTML = data;
    });

  // --- Footer ---
  fetch("footer.html")
    .then(response => response.text())
    .then(data => {
      document.getElementById("footer-container").innerHTML = data;
    });

  // --- Login Form ---
  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener('submit', function(event) {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      fetch('http://localhost:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      })
      .then(response => response.json())
      .then(data => {
        console.log('Server response:', data);
        if (data.access_token) {
          // login réussi, stocker le token
          localStorage.setItem('token', data.access_token);
          window.location.href = 'index.html';
        } else {
          alert('Login failed')
        }
        })
      .catch(error => {
        console.error('Error:', error);
        alert('Login failed!');
      });

    });
  }
});
