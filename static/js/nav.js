// script.js

document.addEventListener('DOMContentLoaded', function() {
    const burgerMenu = document.querySelector('.burger-menu');
    const navLinks = document.querySelector('.nav-links');

    burgerMenu.addEventListener('click', function() {
        navLinks.classList.toggle('show');
    });

    // Close the nav-links if a nav-link is clicked (for mobile view)
    document.querySelectorAll('.nav-link').forEach(item => {
        item.addEventListener('click', () => {
            navLinks.classList.remove('show');
        });
    });

    // Ensure nav-links are hidden on larger screens
    function handleResize() {
        if (window.innerWidth >= 768) {
            navLinks.classList.remove('show');
        }
    }

    window.addEventListener('resize', handleResize);
});
