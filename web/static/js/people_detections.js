document.addEventListener('DOMContentLoaded', function () {
  const canvas = document.getElementById('detectionsChart');
  if (!canvas || !Array.isArray(video.detections_per_frame)) {
    console.error('Not valid data found for the chart');
    return;
  }

  const detectionsData = video.detections_per_frame;

  const labels = detectionsData.map(item => item[0]); // Frames
  const data = detectionsData.map(item => item[1]);   // Nº detections

  const ctx = canvas.getContext('2d');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Detections per frame',
        data: data,
        backgroundColor: '#2563eb',
        borderRadius: 4,
        barPercentage: 0.9
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0
          }
        }
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: '#1f2937',
          titleColor: '#fff',
          bodyColor: '#fff'
        }
      }
    }
  });
});
