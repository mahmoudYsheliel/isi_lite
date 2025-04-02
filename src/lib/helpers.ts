export function fuzzySearch(query:string, items:string[]) {
    // Normalize the query
    const normalizedQuery = query.toLowerCase();

    return items
        .map(item => {
            const normalizedItem = item.toLowerCase();
            const score = calculateScore(normalizedQuery, normalizedItem);
            return { item, score };
        })
        .filter(result => result.score > 0) // Filter out irrelevant results
        .sort((a, b) => b.score - a.score) // Sort by highest score
        .map(result => result.item);
}

// Function to calculate a fuzzy match score
function calculateScore(query:string, target:string) {
    let queryIndex = 0;
    let score = 0;

    for (let targetIndex = 0; targetIndex < target.length; targetIndex++) {
        if (queryIndex < query.length && query[queryIndex] === target[targetIndex]) {
            score++; // Match found
            queryIndex++; // Move to the next character in the query
        }
    }

    return queryIndex === query.length ? score : 0; // Full query matched
}