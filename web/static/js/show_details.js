function toggleInfoDetails() {
        const panel = document.getElementById('stats-details');
        const button = document.getElementById('toggle-info-btn');

        panel.classList.toggle('open');

        if (panel.classList.contains('open')) {
            button.textContent = 'Hide additional stats';
        } else {
            button.textContent = 'Show additional stats';
        }
    }

function toggleModelDetails() {
        const panel = document.getElementById('model-details');
        const button = document.getElementById('toggle-model-btn');

        panel.classList.toggle('open');

        if (panel.classList.contains('open')) {
            button.textContent = 'Hide model details';
        } else {
            button.textContent = 'Show model details';
        }
    }