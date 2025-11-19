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

  async function fetchPlaces(token) {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      const data = await response.json();
      console.log(data);
      return displayPlaces(data);

    } catch (error) {
      console.error("Error fetching places:", error);
    }
  }

  function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';

    if (!places || places.length === 0) {
      placesList.innerHTML = "<p>No place found</p>";
      return;
    }

    places.forEach(place => {
      const card = document.createElement("div");
      card.dataset.price = place.price;
      card.classList.add("place-card");

      card.innerHTML = `
        <img src="${place.image_url || 'images/first_house.jpg'}"
            alt="${place.title}" width="700" height="400">

        <h2 class="place-name">${place.title}</h2>

        <div class="price-wrapper">
          <p class="place-price">${place.price}</p>
          <p class="place-price-text">/night</p>
        </div>

        <button class="details-button"
          onclick="location.href='place.html?id=${place.id}'">View details</button>
      `;

      placesList.appendChild(card);
    });
  }

  const priceFilter = document.getElementById('price-filter');
  ['All', 100, 50, 10].forEach(value => {
    const option = document.createElement('option');
    option.value = value;
    option.textContent = value;
    priceFilter.appendChild(option);
  });
  
  priceFilter.addEventListener('change', (event) => {
    const maxPrice = event.target.value;
    const cards = document.querySelectorAll('.place-card');

    cards.forEach(card => {
      const price = parseFloat(card.dataset.price);

      if (maxPrice === 'All' || price <= parseFloat(maxPrice)) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  });
});

