function downloadQueriesAsExcel() {
    const cachedQueries = JSON.parse(localStorage.getItem("queries")) || [];
    if (cachedQueries.length === 0) {
        alert("No hay consultas almacenadas para descargar.");
        return;
    }

    // Transformar los datos para que sean legibles en Excel
    const excelData = cachedQueries.map(query => ({
        "Sequence": query.sequence,
        "SVM Probability": query.prediction.SVM_probability ?? "N/A", // Acceder a prediction.SVM_probability
        "RF Probability": query.prediction.RandomForest_probability ?? "N/A",
        "NN Probability": query.prediction.NeuralNetwork_probability ?? "N/A",
        "Average Probability": query.prediction.average_probability ?? "N/A",
        "Final Prediction": query.prediction.final_prediction ?? "N/A"
    }));

    // Crear un libro de Excel y una hoja
    const workbook = XLSX.utils.book_new();
    const worksheet = XLSX.utils.json_to_sheet(excelData);

    // Agregar la hoja al libro
    XLSX.utils.book_append_sheet(workbook, worksheet, "querry");

    // Generar el archivo y descargarlo
    XLSX.writeFile(workbook, "querry.xlsx");
}
