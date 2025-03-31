console.log('marquee.js loaded');
document.addEventListener('DOMContentLoaded', () => {
  const ticker = document.getElementById('guildford-ticker');
  if (!ticker) return;

  fetch("https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Guildford?unitGroup=metric&key=GCJSPTBRLERKVDUSZFJZZTL7Y&contentType=json")
    .then(res => res.json())
    .then(data => {
      const current = data.currentConditions;
      const tomorrow = data.days?.[1];

      if (current && tomorrow) {
        ticker.innerText = `Guildford Now: ${current.temp}°C ${current.conditions}; Tomorrow: ${tomorrow.temp}°C ${tomorrow.conditions}`;
      } else {
        ticker.innerText = "Guildford weather not available.";
      }
    })
    .catch(() => {
      ticker.innerText = "Error loading Guildford weather.";
    });
});
