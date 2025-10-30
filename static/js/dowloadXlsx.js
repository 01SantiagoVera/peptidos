function downloadQueriesAsExcel() {
    const cachedQueries = JSON.parse(localStorage.getItem("queries")) || [];
    if (cachedQueries.length === 0) {
        alert("No hay consultas almacenadas para descargar.");
        return;
    }

    // Transformar los datos para que sean legibles en Excel
    const toPercent = (v) => (typeof v === 'number' ? `${(v * 100).toFixed(2)}%` : (v ?? 'N/A'));

    const excelData = cachedQueries.flatMap(query => {
        // Verificar que 'sequence' sea un array
        if (!Array.isArray(query.sequence)) {
            console.warn("El campo 'sequence' no es un array:", query);
            return []; // Ignorar entradas malformadas
        }

        // ✅ Versión ajustada: manejar array plano de objetos
        // Antes: query.sequence.flatMap(innerArray => innerArray.map(...))
        // Ahora: solo map directo
        return query.sequence.map(prediction => ({
            "Input Sequence": prediction.input_sequence || "N/A",
            "SVM Probability": toPercent(prediction.SVM_probability),
            "RF Probability": toPercent(prediction.RandomForest_probability),
            "NN Probability": toPercent(prediction.NeuralNetwork_probability),
            "Average Probability": toPercent(prediction.average_probability),
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
        // Crear libro y hoja de Excel
        const workbook = XLSX.utils.book_new();
        const worksheet = XLSX.utils.json_to_sheet(excelData);

        // Agregar hoja y exportar
        XLSX.utils.book_append_sheet(workbook, worksheet, "Queries");
        XLSX.writeFile(workbook, "queries.xlsx");
    } catch (error) {
        console.error("Error al generar el archivo Excel:", error);
        alert("Ocurrió un error al exportar los datos a Excel. Revisa la consola para más detalles.");
    }
}
