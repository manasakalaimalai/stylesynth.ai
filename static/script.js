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

function redirectToProduct(link) {
    window.open(link, '_blank');
}


window.addEventListener('DOMContentLoaded', function() {
    const resultsContainer = document.querySelector('.results-container');
    resultsContainer.classList.add('loaded');
});


    const textColumns = document.querySelectorAll('.text1-column, .text2-column');

    const options = {
        rootMargin: '0px',
        threshold: 0.3 // Adjust as needed
    };

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInAnimation ease 1s forwards';
                observer.unobserve(entry.target);
            }
        });
    }, options);

    textColumns.forEach(column => {
        observer.observe(column);
    });
