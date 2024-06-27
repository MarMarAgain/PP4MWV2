document.addEventListener('DOMContentLoaded', function() {
    const burgerMenu = document.querySelector('.burger-menu');
    const navLinks = document.querySelector('.nav-links');

    burgerMenu.addEventListener('click', function() {
        navLinks.classList.toggle('open'); // Toggle the 'open' class on navLinks
    });

    // Close the nav-links if a nav-link is clicked (for mobile view)
    document.querySelectorAll('.nav-link').forEach(item => {
        item.addEventListener('click', () => {
            navLinks.classList.remove('open'); // Ensure navLinks is closed on click
        });
    });
});
