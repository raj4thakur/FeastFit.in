// Function to filter recipes based on selected filters
function filterRecipes() {
    const cuisine = document.getElementById('cuisine').value;
    const ingredient = document.getElementById('ingredient').value;
    const diet = document.getElementById('diet').value;
    
    let url = window.location.pathname + '?';
    
    if (cuisine) url += `cuisine=${cuisine}&`;
    if (ingredient) url += `ingredient=${ingredient}&`;
    if (diet) url += `diet=${diet}&`;

    window.location.href = url;  // This will reload the page with the updated filter parameters
}

// Function to handle search functionality
function searchRecipes() {
    const searchTerm = document.getElementById('search').value;
    let url = window.location.pathname + '?';

    if (searchTerm) {
        url += `search=${searchTerm}&`;
    }
    window.location.href = url;  // This will reload the page with the updated search parameter
}
