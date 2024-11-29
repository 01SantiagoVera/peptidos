function cacheQuery(sequence, results) {
    const cachedQueries = JSON.parse(localStorage.getItem('queries')) || [];
    cachedQueries.push({ sequence, prediction: results });
    localStorage.setItem('queries', JSON.stringify(cachedQueries));

    // Llamamos a addToTable con los datos actuales
    addToTable([{ prediction: results }]);
}
