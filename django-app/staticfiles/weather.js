document.addEventListener('DOMContentLoaded', () => {
  const cityBoxes = document.querySelectorAll('.weather-card');

  // Scroll to newly added city
  const scrollId = sessionStorage.getItem('scrollToCity');
  if (scrollId) {
    const newBox = document.querySelector(`.weather-card[data-pk="${scrollId}"]`);
    if (newBox) newBox.scrollIntoView({ behavior: 'smooth' });
    sessionStorage.removeItem('scrollToCity');
  }

  // Fetch weather for each city
  cityBoxes.forEach(box => {
    const cityId = box.dataset.pk;
    const cityName = box.querySelector('.title').textContent.trim();

    fetch(`/proxy/${encodeURIComponent(cityName)}/`)
      .then(res => res.json())
      .then(data => {
        const today = data.currentConditions || data.days?.[0];
        if (!today) return;

        const temp = today.temp;
        const vibe = today.conditions || 'Unknown';
        const desc = today.description || '';
        const iconRaw = today.icon?.toLowerCase() || 'none';
        const iconFile = resolveWeatherIcon(iconRaw);

        box.querySelector(`#deg-${cityId}`).textContent = `${temp}°C`;
        box.querySelector(`#summary-${cityId}`).textContent = vibe;
        box.querySelector('img').src = `/media/${iconFile}`;

        const extra = document.createElement('p');
        extra.className = 'is-size-7 has-text-grey mt-1';
        extra.innerText = desc;
        box.querySelector('.content').appendChild(extra);

        box.style.opacity = 0;
        setTimeout(() => {
          box.style.transition = 'opacity 0.5s';
          box.style.opacity = 1;
        }, 30);
      })
      .catch(err => console.warn('weather fail:', err));
  });

  // Delete city
  document.querySelectorAll('.delete[data-remove]').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.remove;
      fetch(`/ajax/delete/${id}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCSRFToken() }
      })
        .then(res => res.json())
        .then(data => {
          if (data.status === 'ok') {
            showMessage('City deleted.', 'is-success');
            setTimeout(() => location.reload(), 600);
          } else {
            showMessage(data.msg || 'Delete failed', 'is-danger');
          }
        })
        .catch(() => showMessage('Delete failed', 'is-danger'));
    });
  });

  // Add city
  const form = document.querySelector('#addCityForm');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const formData = new FormData(form);
      fetch('/ajax/add/', {
        method: 'POST',
        body: formData,
        headers: { 'X-CSRFToken': getCSRFToken() }
      })
        .then(res => res.json())
        .then(data => {
          if (data.status === 'ok') {
            sessionStorage.setItem('scrollToCity', data.city.id);
            showMessage('City added!', 'is-success');
            setTimeout(() => location.reload(), 600);
          } else {
            const msg = typeof data.errors === 'string' ? data.errors : 'Invalid city name';
            showMessage(msg, 'is-danger');
          }
        })
        .catch(() => showMessage('Something went wrong', 'is-danger'));
    });
  }
});

// Maps raw icon keywords to available icons
function resolveWeatherIcon(keyword) {
  const availableIcons = [
    'clear-day', 'clear-night', 'cloudy', 'fog', 'hail', 'partly-cloudy-day',
    'partly-cloudy-night', 'rain', 'rain-snow', 'rain-snow-showers-day',
    'rain-snow-showers-night', 'showers-day', 'showers-night', 'sleet',
    'snow', 'snow-showers-day', 'snow-showers-night', 'thunder', 'thunder-rain',
    'thunder-showers-day', 'thunder-showers-night', 'wind'
  ];
  for (const icon of availableIcons) {
    if (keyword.includes(icon)) return `${icon}.png`;
  }
  return 'none.png';
}

function getCSRFToken() {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : '';
}

// Show Bulma-style message directly under the form
function showMessage(msg, type = 'is-info') {
  const box = document.getElementById('formMsg');
  if (!box) return;

  box.innerHTML = `
    <div class="notification ${type}">
      <button class="delete"></button>
      ${msg}
    </div>
  `;
  box.querySelector('.delete').onclick = () => box.innerHTML = '';
  setTimeout(() => box.innerHTML = '', 4000);
}
