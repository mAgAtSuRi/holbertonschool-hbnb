document.addEventListener('DOMContentLoaded', () => {
  const path = window.location.pathname;

  // --- COOKIE UTILS ---
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';')[0];
    return null;
  }

  // --- GET PLACE ID FROM URL ---
  function getPlaceIdFromURL() {
    const searchParams = new URLSearchParams(window.location.search);
    return searchParams.get('id');
  }

  // --- LOGIN / LOGOUT AUTHENTICATION ---
  function checkAuthentification() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!loginLink) return token;

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
    }

    return token;
  }

  // --- REVIEWS AUTHENTICATION ---
  function checkAuthenticationReviews(token, placeId) {
    const addReviewSection = document.getElementById('add-review');
    if (!addReviewSection) return;

    if (!token) {
      // User not logged in → hide form
      addReviewSection.style.display = 'none';
    } else {
      // User logged in → show form
      addReviewSection.style.display = 'block';
    }

    fetchPlaceDetails(token, placeId);
  }

  // --- HEADER ---
  fetch("header.html")
    .then(response => response.text())
    .then(data => {
      document.getElementById("header-container").innerHTML = data;
      const token = checkAuthentification();
      fetchPlaces(token);
    });

  // --- FOOTER ---
  fetch("footer.html")
    .then(response => response.text())
    .then(data => {
      document.getElementById("footer-container").innerHTML = data;
    });

  // --- LOGIN FORM ---
  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener('submit', function(event) {
      event.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      fetch('http://localhost:5000/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      .then(response => response.json())
      .then(data => {
        if (data.access_token) {
          document.cookie = `token=${data.access_token}; path=/; max-age=86400`;
          window.location.href = 'index.html';
        } else {
          alert('Login failed');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Login failed!');
      });
    });
  }

  // --- FETCH AND DISPLAY ALL PLACES ---
  async function fetchPlaces(token) {
    try {
      let options = {};
      if (token) options.headers = { 'Authorization': 'Bearer ' + token };

      const response = await fetch('http://127.0.0.1:5000/api/v1/places/', options);
      const data = await response.json();
      displayPlaces(data);
    } catch (error) {
      console.error("Error fetching places:", error);
    }
  }

  function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;
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

  // --- FETCH PLACE DETAILS ---
  async function fetchPlaceDetails(token, placeId) {
    if (!placeId) return;
    try {
      let options = {};
      if (token) options.headers = { 'Authorization': 'Bearer ' + token };

      const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/`, options);
      const data = await response.json();
      displayPlaceDetails(data);
    } catch (error) {
      console.error("Error fetching place details:", error);
    }
  }

  // --- DISPLAY PLACE DETAILS ---
  function displayPlaceDetails(place) {
    const placeDetailsSection = document.querySelector('.place-details');
    if (!placeDetailsSection) return;
    placeDetailsSection.innerHTML = '';

    const title = document.createElement('h2');
    title.textContent = place.title;

    const host = document.createElement('p');
    host.textContent = `Hosted by: ${place.host_name || 'Unknown'}`;

    const price = document.createElement('p');
    price.textContent = `Price: ${place.price}$ per night`;

    const description = document.createElement('p');
    description.textContent = `Description: ${place.description || 'No description available.'}`;

    placeDetailsSection.append(title, host, price, description);

    // --- AMENITIES ---
    const amenitiesSection = document.querySelector('.place-info ul');
    if (amenitiesSection) {
      amenitiesSection.innerHTML = '';
      (place.amenities || []).forEach(amenity => {
        const li = document.createElement('li');
        li.textContent = amenity.name;
        amenitiesSection.appendChild(li);
      });
    }

    // --- REVIEWS ---
    const reviewsSection = document.getElementById('reviews');
    if (reviewsSection) {
      reviewsSection.querySelectorAll('.review-card').forEach(card => card.remove());
      (place.reviews || []).forEach(review => {
        const card = document.createElement('div');
        card.classList.add('review-card');

        const text = document.createElement('p');
        text.textContent = `"${review.text}"`;

        const author = document.createElement('p');
        author.innerHTML = `<strong>${review.user_name}</strong>`;

        const rating = document.createElement('p');
        rating.textContent = `Rating: ${review.rating}/5`;

        card.append(text, author, rating);
        reviewsSection.appendChild(card);
      });
    }
  }

  // --- PRICE FILTER ---
  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    ['All', 100, 50, 10].forEach(value => {
      const option = document.createElement('option');
      option.value = value;
      option.textContent = value;
      priceFilter.appendChild(option);
    });

    priceFilter.addEventListener('change', (event) => {
      const maxPrice = event.target.value;
      document.querySelectorAll('.place-card').forEach(card => {
        const price = parseFloat(card.dataset.price);
        card.style.display = (maxPrice === 'All' || price <= parseFloat(maxPrice)) ? 'block' : 'none';
      });
    });
  }

  // --- EXECUTE TASK 3 ---
  if (path.includes('place.html')) {
    const placeId = getPlaceIdFromURL();
    const token = getCookie('token');
    checkAuthenticationReviews(token, placeId);
  }

});
