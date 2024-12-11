
    const fileInput = document.getElementById('fileInput');
    const textInput = document.getElementById('textInput');
    const fileIndicator = document.getElementById('fileIndicator');

    fileInput.addEventListener('change', (event) => {
        if (event.target.files.length > 0) {
            const fileName = event.target.files[0].name;
            textInput.value = fileName;
            fileIndicator.classList.remove('d-none');
            fileIndicator.textContent = `Loaded: ${fileName}`;
        }
    });

    // Implementar arrastrar y soltar
    const form = document.getElementById('prediction-form');
    form.addEventListener('dragover', (event) => {
        event.preventDefault();
        form.classList.add('dragging');
    });

    form.addEventListener('dragleave', () => {
        form.classList.remove('dragging');
    });

    form.addEventListener('drop', (event) => {
        event.preventDefault();
        form.classList.remove('dragging');
        if (event.dataTransfer.files.length > 0) {
            const file = event.dataTransfer.files[0];
            fileInput.files = event.dataTransfer.files;
            textInput.value = file.name;
            fileIndicator.classList.remove('d-none');
            fileIndicator.textContent = `Loaded: ${file.name}`;
        }
    });