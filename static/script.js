function toggleDropdown() {
    var dropdown = document.getElementById("dropdown");
    dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
}


// JavaScript to handle tag creation and search
document.addEventListener("DOMContentLoaded", function () {
    const selects = document.querySelectorAll(".dropdown select");
    const searchInput = document.getElementById("search");
    
    selects.forEach(select => {
        select.addEventListener("change", function () {
            const selectedOption = select.options[select.selectedIndex];
            
            if (selectedOption.value !== "") {
                const tagText = selectedOption.text;
                const currentValue = searchInput.value.trim();
                
                if (currentValue === "") {
                    searchInput.value = tagText;
                } else {
                    searchInput.value = currentValue + ", " + tagText;
                }
                
                selectedOption.disabled = true;
                select.selectedIndex = 0;
            }
        });
    });
});
