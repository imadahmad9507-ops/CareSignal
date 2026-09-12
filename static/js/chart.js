const observations = window.trendData || [];
const canvas = document.getElementById('trendChart');

if (canvas && observations.length) {
  new Chart(canvas, {
    type: 'line',
    data: {
      labels: observations.map(item => item.date),
      datasets: [
        { label: 'Oxygen %', data: observations.map(item => item.oxygen), borderColor: '#2f8f62', backgroundColor: '#2f8f62', borderWidth: 2, pointRadius: 4, pointHoverRadius: 6, showLine: true, fill: false, tension: 0.3, yAxisID: 'oxygen' },
        { label: 'Temperature °C', data: observations.map(item => item.temperature), borderColor: '#d8773f', backgroundColor: '#d8773f', borderWidth: 2, pointRadius: 4, pointHoverRadius: 6, showLine: true, fill: false, tension: 0.3, yAxisID: 'temperature' },
        { label: 'Pain / 10', data: observations.map(item => item.pain_level), borderColor: '#17221f', backgroundColor: '#17221f', borderWidth: 2, pointRadius: 4, pointHoverRadius: 6, showLine: true, fill: false, tension: 0.3, yAxisID: 'pain' }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false } },
        oxygen: {
          type: 'linear',
          position: 'left',
          suggestedMin: 80,
          suggestedMax: 100,
          title: { display: true, text: 'Oxygen %', color: '#2f8f62' },
          ticks: { stepSize: 5 }
        },
        temperature: {
          type: 'linear',
          position: 'right',
          suggestedMin: 35,
          suggestedMax: 41,
          grid: { drawOnChartArea: false },
          title: { display: true, text: 'Temperature °C', color: '#d8773f' },
          ticks: { stepSize: 1 }
        },
        pain: {
          type: 'linear',
          position: 'right',
          suggestedMin: 0,
          suggestedMax: 10,
          grid: { drawOnChartArea: false },
          title: { display: true, text: 'Pain / 10', color: '#17221f' },
          ticks: { stepSize: 2 }
        }
      }
    }
  });
}
