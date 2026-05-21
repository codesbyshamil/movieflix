// static/js/script.js

/**
 * Show movies belonging to the selected category.
 * Also updates the active state on category buttons.
 *
 * @param {string} category - Genre name or "all"
 * @param {HTMLElement} btn  - The clicked button element
 */
function showCategory(category, btn) {

    // Update active button
    document.querySelectorAll(".cat-btn").forEach(b => b.classList.remove("active"));
    if (btn) btn.classList.add("active");

    const sections = document.querySelectorAll(".movie-section");

    // Show all sections
    if (category === "all") {
        sections.forEach(section => section.style.display = "block");
        return;
    }

    // Hide all, then show selected
    sections.forEach(section => section.style.display = "none");

    const selected = document.getElementById(category);
    if (selected) selected.style.display = "block";
}


/**
 * Redirect to the logout route.
 */
function logout() {
    window.location.href = "/logout";
}
