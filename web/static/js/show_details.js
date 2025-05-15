function toggleInfoDetails() {
        const panel = document.getElementById('stats-details');
        const button = document.getElementById('toggle-info-btn');

        panel.classList.toggle('open');

        if (panel.classList.contains('open')) {
            button.textContent = 'Ocultar estadísticas extra';
        } else {
            button.textContent = 'Mostrar estadísticas extra';
        }
    }

function toggleModelDetails() {
        const panel = document.getElementById('model-details');
        const button = document.getElementById('toggle-model-btn');

        panel.classList.toggle('open');

        if (panel.classList.contains('open')) {
            button.textContent = 'Ocultar detalles del modelo';
        } else {
            button.textContent = 'Mostrar detalles del modelo';
        }
    }