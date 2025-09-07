// script.js

document.addEventListener("DOMContentLoaded", function () {
    const animatedElements = document.querySelectorAll('.animated');

    function checkScroll() {
        animatedElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const isVisible = elementTop < window.innerHeight;

            if (isVisible) {
                element.classList.add('visible');
            } else {
                element.classList.remove('visible');
            }
        });
    }

    window.addEventListener("scroll", checkScroll);
    checkScroll(); // Trigger the check on page load
});
