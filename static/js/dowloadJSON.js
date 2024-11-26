function cacheQuery(sequence, results) {
    const cachedQueries = JSON.parse(localStorage.getItem("queries")) || [];
    cachedQueries.push({ sequence, ...results }); // Almacenar el objeto completo
    localStorage.setItem("queries", JSON.stringify(cachedQueries));
}
