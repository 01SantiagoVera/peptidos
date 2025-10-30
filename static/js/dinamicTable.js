function addToTable(data) {
    console.log(data); // Imprime la estructura de 'data' para depuración
    const container = document.getElementById("results-container");
    const table = document.getElementById("results-table");
    const tbody = table.querySelector("tbody");

    // Mostrar el contenedor si está oculto
    if (container.style.display === 'none' || container.style.display === '') {
        container.style.display = 'block'; // Muestra el contenedor
    }

    // Aplanar el array de predicciones
    const flatData = data.flat();

    // Verificar si 'flatData' es un array
    if (Array.isArray(flatData)) {
        flatData.forEach(seq => {
            console.log(seq); // Imprime cada objeto para ver qué contiene
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
                    if (typeof value === "number") {
                        row.insertCell(-1).textContent = `${(value * 100).toFixed(2)}%`;
                    } else {
                        row.insertCell(-1).textContent = value;
                    }
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
