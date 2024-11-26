function addToTable(sequence, data) {
    const table = document.getElementById("results-table");
    const models = Object.keys(data.prediction).filter(key => key.includes("probability")); // Modelos usados
    const avgProbability = data.prediction.average_probability ?? "N/A"; // Promedio correcto
    const finalPrediction = data.prediction.final_prediction ?? "N/A"; // Conclusión correcta

    // Crear encabezados dinámicos si no existen
    if (table.rows.length === 0) {
        const headerRow = table.createTHead().insertRow(0);
        headerRow.insertCell(0).textContent = "Secuencia";

        // Encabezados para probabilidades de modelos
        models.forEach(model => {
            const modelName = model.replace("_probability", "").replace(/_/g, " "); // Limpiar nombres
            headerRow.insertCell(-1).textContent = `Probabilidad ${modelName}`;
        });

        headerRow.insertCell(-1).textContent = "Promedio";
        headerRow.insertCell(-1).textContent = "Conclusión";
    }

    // Agregar fila con los datos
    const row = table.insertRow();
    row.insertCell(0).textContent = sequence;

    // Valores de los modelos
    models.forEach(model => {
        const value = data.prediction[model] !== undefined ? data.prediction[model] : "No utilizado";
        row.insertCell(-1).textContent = typeof value === "number" ? value.toFixed(2) : value; // Limitar a 2 decimales
    });

    // Promedio y Conclusión en la misma celda
    const lastCell = row.insertCell(-1);
    lastCell.textContent = finalPrediction;
}