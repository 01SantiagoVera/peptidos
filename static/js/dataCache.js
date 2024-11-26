function cacheQuery(sequence, results) {
    const cachedQueries = JSON.parse(localStorage.getItem('queries')) || [];
    cachedQueries.push({ sequence, ...results });
    localStorage.setItem('queries', JSON.stringify(cachedQueries));
}
