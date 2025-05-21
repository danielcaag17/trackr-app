/**
 * @typedef {{ person_id: number, duration: number }} PersonTime
 * @type {{ detections_per_frame: any[], time_per_person: PersonTime[] }}
 */

const top_time = video.time_per_person.sort((a, b) => b.duration - a.duration);
const labels = top_time.map(p => `Person ${p.person_id}`);
const durations = top_time.map(p => p.duration);

const itemsPerPage = 10;
let currentPage = 0;
const ctx = document.getElementById("durationBarChart").getContext("2d");

const max_duration = Math.max(...durations);
let chartInstance;

function renderChartPage(page) {

    const start = page * itemsPerPage;
    const end = start + itemsPerPage;
    const pageLabels = labels.slice(start, end);
    const pageData = durations.slice(start, end);

    if (chartInstance) {
        chartInstance.destroy();
    }

    chartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: pageLabels,
            datasets: [{
                label: "Duration (s)",
                data: pageData,
                backgroundColor: "rgba(54, 162, 235, 0.6)",
                borderColor: "rgba(54, 162, 235, 1)",
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: false,
            maintainAspectRatio: false,
            scales: {
                x: {
                    beginAtZero: true,
                    max: max_duration
                }
            }
        }
    });

    // Update UI
    document.getElementById("pageIndicator").textContent = `Page ${page + 1}`;
    document.getElementById("prevPage").disabled = page === 0;
    document.getElementById("nextPage").disabled = end >= labels.length;
}

document.getElementById("prevPage").addEventListener("click", () => {
    if (currentPage > 0) {
        currentPage--;
        renderChartPage(currentPage);
    }
});

document.getElementById("nextPage").addEventListener("click", () => {
    if ((currentPage + 1) * itemsPerPage < labels.length) {
        currentPage++;
        renderChartPage(currentPage);
    }
});

// Inicialización
renderChartPage(currentPage);

