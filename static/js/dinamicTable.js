function addToTable(data) {
    const container = document.getElementById("results-container");
    const table = document.getElementById("results-table");
    const tbody = table.querySelector("tbody");

    // Mostrar el contenedor si está oculto
    if (container.style.display === 'none' || container.style.display === '') {
        container.style.display = 'block'; // Muestra el contenedor
    }

    // Verificar si 'data' es un array
    if (Array.isArray(data)) {
        data.forEach(seq => {
            if (seq && seq.input_sequence) { // Verificar que 'seq' tenga 'input_sequence'
                const sequence = seq.input_sequence; // Usar 'input_sequence' directamente

                const models = Object.keys(seq).filter(key => key.includes("probability"));
                const avgProbability = seq.average_probability ?? "N/A";
                const finalPrediction = seq.final_prediction ?? "N/A";

                // Agregar fila con los datos
                const row = tbody.insertRow();
                row.insertCell(0).textContent = sequence;

                // Agregar los valores de los modelos
                models.forEach(model => {
                    const value = seq[model] !== undefined ? seq[model] : "No utilizado";
                    row.insertCell(-1).textContent = typeof value === "number" ? value.toFixed(2) : value;
                });

                // Agregar la conclusión
                row.insertCell(-1).textContent = finalPrediction;
            } else {
                console.error("El objeto 'seq' no tiene 'input_sequence'", seq);
            }
        });
    } else {
        console.error("Se esperaba un array para 'data', pero se recibió:", data);
        alert("Hubo un error al procesar los datos de predicción.");
    }
}
