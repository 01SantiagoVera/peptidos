function addToTable(sequence, data) {
    const container = document.getElementById("results-container");
    const table = document.getElementById("results-table");
    const tbody = table.querySelector("tbody");

     // Mostrar el contenedor si está oculto
    if (container.style.display === 'none' || container.style.display === '') {
        container.style.display = 'block'; // Muestra el contenedor
    }

    const models = Object.keys(data.prediction).filter(key => key.includes("probability"));
    const avgProbability = data.prediction.average_probability ?? "N/A";
    const finalPrediction = data.prediction.final_prediction ?? "N/A";

    // Agregar fila con los datos
    const row = tbody.insertRow();
    row.insertCell(0).textContent = sequence;

    // Valores de los modelos
    models.forEach(model => {
        const value = data.prediction[model] !== undefined ? data.prediction[model] : "No utilizado";
        row.insertCell(-1).textContent = typeof value === "number" ? value.toFixed(2) : value;
    });

    // Agregar conclusión
    row.insertCell(-1).textContent = finalPrediction;
}
