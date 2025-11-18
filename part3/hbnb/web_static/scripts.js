document.addEventListener('DOMContentLoaded', () => {
  // --- Header ---
  fetch("header.html")
    .then(response => response.text())
    .then(data => {
      document.getElementById("header-container").innerHTML = data;
      checkAuthentification();
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
          // login réussi, Stocker le token dans un cookie
          document.cookie = `token=${data.access_token}; path=/; max-age=86400`;;
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

  // ---AUTH CHECK---
  function checkAuthentification() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
      loginLink.textContent = "Login";
      loginLink.href = "login.html";
      loginLink.onclick = null;
    } else {
      loginLink.textContent = "Logout";  

      loginLink.onclick = function(event) {
        event.preventDefault();
        document.cookie = "token=; Max-Age=0; path=/";
        window.location.reload();
      };
      fetchPlaces(token);
    }
  }
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';')[0];
  }
});

