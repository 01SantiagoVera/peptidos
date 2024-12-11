function cacheQuery(predictions) {
    console.log("Predicciones recibidas:", predictions);

    try {
        // Recuperar consultas almacenadas en localStorage
        const cachedQueries = JSON.parse(localStorage.getItem('queries')) || [];

        // Aplanar el array de predicciones (eliminando el nivel adicional de array)
        const flatPredictions = predictions.flat();  // Esto aplana el array de un solo nivel

        // Iterar sobre las predicciones
        flatPredictions.forEach(({ input_sequence, final_prediction }) => {
            // Verificar si ya existe la secuencia en el caché
            const exists = cachedQueries.some(query => query.sequence === input_sequence);

            if (!exists) {
                // Agregar al caché si no existe
                cachedQueries.push({
                    sequence: input_sequence,
                    prediction: final_prediction,
                    timestamp: new Date().toISOString()
                });
            }
        });

        // Guardar el caché actualizado en localStorage
        try {
            localStorage.setItem('queries', JSON.stringify(cachedQueries));
        } catch (error) {
            console.error("No se pudo guardar en localStorage:", error);
            alert("Hubo un problema al guardar las predicciones en el almacenamiento local.");
        }
        console.log("Datos pasados a addToTable:", flatPredictions);

        // Actualizar la tabla en la interfaz
        addToTable(flatPredictions);
    } catch (error) {
        console.error("Error al guardar en localStorage:", error);
    }
}
