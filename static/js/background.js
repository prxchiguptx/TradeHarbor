
window.addEventListener('scroll', function() {
    if (window.scrollY > 0) { // Check if user has scrolled down
      document.querySelector('.background-container').classList.add('blur'); // Apply blur
    } else {
      document.querySelector('.background-container').classList.remove('blur'); // Remove blur if scrolled to top
    }
  });
