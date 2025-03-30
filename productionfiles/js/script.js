// Check if we're on the home page before running the slider JS
if (document.body.classList.contains('home-page')) {
   let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const totalSlides = slides.length;

const prevButton = document.querySelector('.prev');
const nextButton = document.querySelector('.next');

// Show the next slide
function showNextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    updateSliderPosition();
}

// Show the previous slide
function showPrevSlide() {
    currentSlide = (currentSlide - 1 + totalSlides) % totalSlides;
    updateSliderPosition();
}

// Update slider position
function updateSliderPosition() {
    const newTransformValue = -currentSlide * 100; // Move slides horizontally
    document.querySelector('.slides-container').style.transform = `translateX(${newTransformValue}%)`;
}

// Event listeners for buttons
nextButton.addEventListener('click', showNextSlide);
prevButton.addEventListener('click', showPrevSlide);

// Automatically slide every 5 seconds
setInterval(showNextSlide, 5000); 

}

// Function for uploading videos (will work across pages)
function uploadVideo() {
    const videoFile = document.getElementById('videoFile').files[0];
    if (videoFile) {
        alert('Video uploaded: ' + videoFile.name);
        // Here, you can handle the logic for uploading the video to the server
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('appointmentForm');
    if (form) { // Check if the form exists on the page
        form.addEventListener('submit', function(e) {
            let isValid = true;

            // Validate all required fields
            document.querySelectorAll('input[required]').forEach(function(input) {
                if (!input.value) {
                    isValid = false;
                    alert(input.placeholder + ' is required!');
                }
            });

            // Email validation (additional check)
            let email = document.querySelector('input[name="email"]').value;
            const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
            if (!emailPattern.test(email)) {
                isValid = false;
                alert('Please enter a valid email address!');
            }

            // US phone validation (additional check)
            //let phone = document.querySelector('input[name="phone"]').value;
            //const phonePattern = /(\(\d{3}\)\s?|\d{3}[-\s])\d{3}[-\s]?\d{4}/;
            //if (!phonePattern.test(phone)) {
            //    isValid = false;
            //    alert('Please enter a valid US phone number!');
           // }

            if (!isValid) {
                e.preventDefault(); // Prevent form submission
            }
        });
    }
});

// Toggle mobile menu
function toggleMenu() {
    const menuItems = document.getElementById('menu-items');
    menuItems.classList.toggle('active');
}

// Handle slider functionality if one exists
document.addEventListener('DOMContentLoaded', function() {
    const slidesContainer = document.querySelector('.slides-container');
    
    if (slidesContainer) {
        const slides = document.querySelectorAll('.slide');
        const prevButton = document.querySelector('.prev');
        const nextButton = document.querySelector('.next');
        let currentIndex = 0;
        const slideCount = slides.length;
        
        // Auto-advance the slider every 5 seconds
        let slideInterval = setInterval(nextSlide, 5000);
        
        function updateSlidePosition() {
            slidesContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
        }
        
        function nextSlide() {
            currentIndex = (currentIndex + 1) % slideCount;
            updateSlidePosition();
        }
        
        function prevSlide() {
            currentIndex = (currentIndex - 1 + slideCount) % slideCount;
            updateSlidePosition();
        }
        
        // Add event listeners if buttons exist
        if (prevButton) {
            prevButton.addEventListener('click', function() {
                clearInterval(slideInterval);
                prevSlide();
                slideInterval = setInterval(nextSlide, 5000);
            });
        }
        
        if (nextButton) {
            nextButton.addEventListener('click', function() {
                clearInterval(slideInterval);
                nextSlide();
                slideInterval = setInterval(nextSlide, 5000);
            });
        }
    }
    
    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add active class to current nav item
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('nav ul li a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentLocation) {
            link.parentElement.classList.add('active');
        }
    });
    
    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            let isValid = true;
            
            // Check required fields
            const requiredFields = form.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                    
                    // Add error message if it doesn't exist
                    let errorMsg = field.nextElementSibling;
                    if (!errorMsg || !errorMsg.classList.contains('error-message')) {
                        errorMsg = document.createElement('small');
                        errorMsg.classList.add('error-message');
                        errorMsg.textContent = 'This field is required';
                        field.parentNode.insertBefore(errorMsg, field.nextSibling);
                    }
                } else {
                    field.classList.remove('error');
                    
                    // Remove error message if it exists
                    const errorMsg = field.nextElementSibling;
                    if (errorMsg && errorMsg.classList.contains('error-message')) {
                        errorMsg.remove();
                    }
                }
            });
            
            // Check email format
            const emailFields = form.querySelectorAll('input[type="email"]');
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            emailFields.forEach(field => {
                if (field.value.trim() && !emailRegex.test(field.value.trim())) {
                    isValid = false;
                    field.classList.add('error');
                    
                    // Add error message if it doesn't exist
                    let errorMsg = field.nextElementSibling;
                    if (!errorMsg || !errorMsg.classList.contains('error-message')) {
                        errorMsg = document.createElement('small');
                        errorMsg.classList.add('error-message');
                        errorMsg.textContent = 'Please enter a valid email address';
                        field.parentNode.insertBefore(errorMsg, field.nextSibling);
                    }
                }
            });
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    });
    
    // Add fade-in animation to elements as they scroll into view
    const fadeElements = document.querySelectorAll('.fade-in');
    
    const fadeInObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                fadeInObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    fadeElements.forEach(element => {
        fadeInObserver.observe(element);
    });
});

// Back to top button functionality
window.addEventListener('scroll', function() {
    const backToTopButton = document.getElementById('back-to-top');
    
    if (backToTopButton) {
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    }
});

// Copy to clipboard functionality for any element with data-copy attribute
document.addEventListener('click', function(e) {
    if (e.target.hasAttribute('data-copy')) {
        const textToCopy = e.target.getAttribute('data-copy');
        navigator.clipboard.writeText(textToCopy).then(() => {
            // Visual feedback
            const originalText = e.target.textContent;
            e.target.textContent = 'Copied!';
            
            setTimeout(() => {
                e.target.textContent = originalText;
            }, 2000);
        });
    }
});


