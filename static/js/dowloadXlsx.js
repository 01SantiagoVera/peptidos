function downloadQueriesAsExcel() {
    const cachedQueries = JSON.parse(localStorage.getItem("queries")) || [];
    if (cachedQueries.length === 0) {
        alert("No hay consultas almacenadas para descargar.");
        return;
    }

    // Transformar los datos para que sean legibles en Excel
    const excelData = cachedQueries.map(query => ({
        "Secuencia": query.sequence,
        "SVM Probabilidad": query.prediction.SVM_probability,
        "RF Probabilidad": query.prediction.RandomForest_probability,
        "NN Probabilidad": query.prediction.NeuralNetwork_probability,
        "Promedio Probabilidad": query.prediction.average_probability,
        "Conclusión": query.prediction.final_prediction
    }));

    // Crear un libro de Excel y una hoja
    const workbook = XLSX.utils.book_new();
    const worksheet = XLSX.utils.json_to_sheet(excelData);

    // Agregar la hoja al libro
    XLSX.utils.book_append_sheet(workbook, worksheet, "Consultas");

    // Generar el archivo y descargarlo
    XLSX.writeFile(workbook, "consultas.xlsx");
}
