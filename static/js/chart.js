const observations = window.trendData || [];
const canvas = document.getElementById('trendChart');

if (canvas && observations.length) {
  new Chart(canvas, {
    type: 'line',
    data: {
      labels: observations.map(item => item.date),
      datasets: [
        { label: 'Oxygen %', data: observations.map(item => item.oxygen), borderColor: '#2f8f62', backgroundColor: '#2f8f62', tension: 0.3, yAxisID: 'health' },
        { label: 'Temperature °C', data: observations.map(item => item.temperature), borderColor: '#d8773f', backgroundColor: '#d8773f', tension: 0.3, yAxisID: 'temperature' },
        { label: 'Pain / 10', data: observations.map(item => item.pain_level), borderColor: '#17221f', backgroundColor: '#17221f', tension: 0.3, yAxisID: 'health' }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false } },
        health: { min: 0, max: 100, position: 'left', title: { display: true, text: 'Oxygen / pain' } },
        temperature: { min: 30, max: 42, position: 'right', grid: { drawOnChartArea: false }, title: { display: true, text: 'Temperature °C' } }
      }
    }
  });
}
