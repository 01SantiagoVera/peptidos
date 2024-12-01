function downloadQueriesAsExcel() {
    const cachedQueries = JSON.parse(localStorage.getItem("queries")) || [];
    if (cachedQueries.length === 0) {
        alert("No hay consultas almacenadas para descargar.");
        return;
    }

    // Transformar los datos para que sean legibles en Excel
    const excelData = cachedQueries.flatMap(query => {
        if (!Array.isArray(query.prediction)) {
            console.warn("El campo 'prediction' no es un array:", query);
            return []; // Ignorar entradas malformadas
        }

        return query.prediction.map(prediction => ({
            "Input Sequence": prediction.input_sequence || "N/A", // Secuencia individual
            "SVM Probability": prediction.SVM_probability ?? "N/A",
            "RF Probability": prediction.RandomForest_probability ?? "N/A",
            "NN Probability": prediction.NeuralNetwork_probability ?? "N/A",
            "Average Probability": prediction.average_probability ?? "N/A",
            "Final Prediction": prediction.final_prediction ?? "N/A"
        }));
    });

    // Verificar los datos transformados
    console.log("Datos preparados para Excel:", excelData);

    if (excelData.length === 0) {
        alert("No hay datos válidos para exportar.");
        return;
    }

    try {
        // Crear un libro de Excel y una hoja
        const workbook = XLSX.utils.book_new();
        const worksheet = XLSX.utils.json_to_sheet(excelData);

        // Agregar la hoja al libro
        XLSX.utils.book_append_sheet(workbook, worksheet, "Queries");

        // Generar el archivo y descargarlo
        XLSX.writeFile(workbook, "queries.xlsx");
    } catch (error) {
        console.error("Error al generar el archivo Excel:", error);
        alert("Ocurrió un error al exportar los datos a Excel. Revisa la consola para más detalles.");
    }
}
