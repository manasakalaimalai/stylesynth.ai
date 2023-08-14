function toggleDropdown() {
    var dropdown = document.getElementById("dropdown");
    dropdown.style.display = (dropdown.style.display === "block") ? "none" : "block";
}

function populateSearchBar(optionId) {
    var selectedOption = document.getElementById(optionId);
    var searchInput = document.getElementById('search');
    var currentSearchValue = searchInput.value;
    
    // Append the selected option value to the search bar
    if (currentSearchValue === '') {
        searchInput.value = selectedOption.value;
    } else {
        searchInput.value = currentSearchValue + ', ' + selectedOption.value;
    }
}