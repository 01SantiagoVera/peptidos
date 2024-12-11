document.addEventListener('DOMContentLoaded', function() {
    const predictionForm = document.getElementById("prediction-form");
    const textInput = document.getElementById("textInput");
    const fileInput = document.getElementById('fileInput');
    const submitBtn = document.getElementById('submit-btn');
    const fileIndicator = document.getElementById('fileIndicator');

    // Obtener los modelos seleccionados
    const selectedModels = Array.from(document.querySelectorAll('input[name="model"]:checked'))
        .map((checkbox) => checkbox.value);

    // Manejar carga de archivo
    fileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            if (!file.type.match('text.*')) {
                alert("Por favor, selecciona un archivo de texto válido.");
                fileInput.value = ""; // Limpiar el campo de archivo
                return;
            }
            const reader = new FileReader();
            reader.onload = function(e) {
                textInput.value = e.target.result.trim();
                fileIndicator.classList.remove('d-none');
                setTimeout(() => {
                    fileIndicator.classList.add('d-none');
                }, 3000);
            };
            reader.readAsText(file);
        }
    });

    predictionForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        // Deshabilitar botón de envío y mostrar spinner
        submitBtn.disabled = true;
        submitBtn.innerHTML = `
            <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
            Processing...
        `;

        try {
            // Crear un objeto FormData para enviar los datos del formulario
            const formData = new FormData(predictionForm);

            // Agregar secuencia al FormData
            const sequence = textInput.value.trim();
            formData.append('sequence', sequence);

            // Si hay un archivo, agregarlo al FormData
            if (fileInput.files.length > 0) {
                formData.append('file', fileInput.files[0]);
            }

            // Agregar los modelos seleccionados
            formData.append('model', selectedModels);

            // Realizar la solicitud POST al servidor
            const response = await fetch("/api/predict", {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error("Error en la respuesta del servidor.");
            }

            const data = await response.json();
            console.log("Respuesta del servidor:", data);

            if (data.predictions) {
                console.log("Predicciones realizadas con éxito.");
                // Aquí podrías procesar y mostrar los resultados en la interfaz
                console.log("Predicciones recibidas:", data.predictions);
                cacheQuery(data.predictions);
                console.log("Predicciones aplastadas:", data.flatPredictions);


                addToTable(data.predictions);
            } else {
                console.log("No se encontraron resultados de predicción.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Hubo un problema procesando la predicción. Inténtalo de nuevo.");
        } finally {
            // Resetear el botón de envío
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Submit';
        }
    });

    console.log("Archivo cargado:", textInput.value); // Al leer el archivo
    console.log("Modelos seleccionados:", selectedModels); // Antes de enviar
    console.log("Secuencia enviada:", sequence); // Antes del fetch
});
