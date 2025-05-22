document.addEventListener('DOMContentLoaded', function () {
    const input = document.getElementById('video-input');
    const fileNameDisplay = document.getElementById('file-name');

    input.addEventListener('change', function () {
        if (input.files.length > 0) {
            fileNameDisplay.textContent = input.files[0].name;
        } else {
            fileNameDisplay.textContent = 'No file selected';
        }
    });
});
