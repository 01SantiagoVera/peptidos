document.getElementById("prediction-form").addEventListener("submit", async function(event) {
    event.preventDefault(); // Evitar el envío tradicional del formulario

    // Obtener la secuencia ingresada
    const sequence = document.querySelector('input[name="sequence"]').value;

    // Obtener los modelos seleccionados
    const selectedModels = Array.from(document.querySelectorAll('input[name="model"]:checked')).map(input => input.value);

    if (!sequence.trim()) {
        alert("Por favor, ingresa una secuencia válida.");
        return;
    }

    if (selectedModels.length === 0) {
        alert("Por favor, selecciona al menos un modelo.");
        return;
    }

    try {
        // Realizar la solicitud POST
        const response = await fetch("/api/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ sequence, models: selectedModels }) // Enviar modelos seleccionados
        });

        if (!response.ok) {
            throw new Error("Error en la respuesta del servidor.");
        }

        const data = await response.json();
        console.log("Respuesta del servidor:", data);

        // Mostrar resultados y almacenarlos
        addToTable(data.prediction); // Cambiar aquí para enviar el array 'data.prediction'
        cacheQuery(sequence, data);
    } catch (error) {
        console.error("Error:", error);
        alert("Hubo un problema procesando la predicción. Inténtalo de nuevo.");
    }
});
