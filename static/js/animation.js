// animation.js

document.addEventListener("DOMContentLoaded", function () {
    const subpointsContainer = document.querySelector('.subpoints-container');
    const subpoints = document.querySelectorAll('.subpoint');
    const introText = document.querySelector('.intro-text');

    function checkScroll() {
        const containerTop = subpointsContainer.getBoundingClientRect().top;
        const isVisible = containerTop < window.innerHeight;

        if (isVisible) {
            subpointsContainer.classList.add('visible');
            subpoints.forEach((subpoint, index) => {
                setTimeout(() => {
                    subpoint.classList.add('visible');
                }, index * 200); // Adjust the delay between each subpoint
            });

            setTimeout(() => {
                introText.classList.add('visible');
            }, subpoints.length * 200); // Adjust the delay for intro text
        } else {
            subpointsContainer.classList.remove('visible');
            subpoints.forEach(subpoint => {
                subpoint.classList.remove('visible');
            });

            introText.classList.remove('visible');
        }
    }

    window.addEventListener("scroll", checkScroll);
    checkScroll(); // Trigger the check on page load
});
