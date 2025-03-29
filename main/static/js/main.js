// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Slider functionality
    const sliderInit = () => {
        const slider = document.querySelector('.slider');
        const slides = document.querySelectorAll('.slide');
        if (slides.length === 0) return;
        
        const prevBtn = document.querySelector('.prev');
        const nextBtn = document.querySelector('.next');
        let currentSlide = 0;
        
        // Function to show a specific slide with a proper fade transition
        function showSlide(n) {
            // Fade out current slide
            slides[currentSlide].style.opacity = '0';
            
            setTimeout(() => {
                // Hide current slide
                slides[currentSlide].style.display = 'none';
                
                // Calculate new slide index
                currentSlide = (n + slides.length) % slides.length;
                
                // Prepare next slide
                slides[currentSlide].style.opacity = '0';
                slides[currentSlide].style.display = 'block';
                
                // Trigger reflow
                void slides[currentSlide].offsetWidth;
                
                // Fade in next slide
                slides[currentSlide].style.opacity = '1';
            }, 300); // Match this to your CSS transition time
        }
        
        // Initialize all slides to be hidden except the first one
        slides.forEach((slide, index) => {
            if (index === 0) {
                slide.style.display = 'block';
                slide.style.opacity = '1';
            } else {
                slide.style.display = 'none';
                slide.style.opacity = '0';
            }
        });
        
        // Event listeners for prev/next buttons
        if (prevBtn && nextBtn) {
            prevBtn.addEventListener('click', () => {
                showSlide(currentSlide - 1);
            });
            
            nextBtn.addEventListener('click', () => {
                showSlide(currentSlide + 1);
            });
            
            // Auto slide if there are multiple slides
            if (slides.length > 1) {
                let slideInterval = setInterval(() => {
                    showSlide(currentSlide + 1);
                }, 5000);
                
                // Pause slideshow when hovering over slider
                if (slider) {
                    slider.addEventListener('mouseenter', () => {
                        clearInterval(slideInterval);
                    });
                    
                    slider.addEventListener('mouseleave', () => {
                        slideInterval = setInterval(() => {
                            showSlide(currentSlide + 1);
                        }, 5000);
                    });
                }
            }
        }
    };

    // Back to top button functionality
    const backToTopInit = () => {
        const backToTopButton = document.querySelector('.back-to-top');
        if (!backToTopButton) return;
        
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                backToTopButton.style.display = 'flex';
            } else {
                backToTopButton.style.display = 'none';
            }
        });
        
        backToTopButton.addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    };
    
    // Mobile menu toggle
    const mobileMenuInit = () => {
        const menuToggle = document.querySelector('.navbar-toggler');
        const navbarCollapse = document.querySelector('.navbar-collapse');
        
        if (menuToggle && navbarCollapse) {
            menuToggle.addEventListener('click', () => {
                navbarCollapse.classList.toggle('show');
            });
            
            // Close mobile menu when clicking outside
            document.addEventListener('click', (e) => {
                if (navbarCollapse.classList.contains('show') && 
                    !navbarCollapse.contains(e.target) && 
                    !menuToggle.contains(e.target)) {
                    navbarCollapse.classList.remove('show');
                }
            });
        }
    };
    
    // Navbar active state based on current page
    const navbarActiveInit = () => {
        const currentLocation = window.location.pathname;
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href === currentLocation || 
                (href === '/' && currentLocation === '') || 
                (href !== '/' && currentLocation.indexOf(href) !== -1)) {
                link.classList.add('active');
            }
        });
    };
    
    // Form validation
    const formValidationInit = () => {
        const forms = document.querySelectorAll('.needs-validation');
        
        forms.forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
    };
    
    // Initialize all functions
    sliderInit();
    backToTopInit();
    mobileMenuInit();
    navbarActiveInit();
    formValidationInit();
});

// Sticky Navbar
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (window.scrollY > 100) {
            navbar.classList.add('sticky-top');
            navbar.classList.add('shadow');
        } else {
            navbar.classList.remove('shadow');
        }
    }
});

// Mobile Menu Toggle with Bootstrap
document.addEventListener('DOMContentLoaded', function() {
    // For Bootstrap navbar toggler
    const navbarToggler = document.querySelector('.navbar-toggler');
    if (navbarToggler) {
        navbarToggler.addEventListener('click', function() {
            document.querySelector('#navbarCollapse').classList.toggle('show');
        });
    }
    
    // Legacy menu toggle for the old menu if it exists
    const menuToggle = document.querySelector('.menu-toggle');
    const menuItems = document.querySelector('#menu-items');
    
    if (menuToggle && menuItems) {
        menuToggle.addEventListener('click', function() {
            menuItems.classList.toggle('active');
        });
    }
});

// Back to top button
document.addEventListener('DOMContentLoaded', function() {
    const backToTopButton = document.querySelector('.back-to-top');
    
    if (backToTopButton) {
        // Initially hide the button
        backToTopButton.style.display = 'none';
        
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTopButton.style.display = 'block';
            } else {
                backToTopButton.style.display = 'none';
            }
        });
        
        backToTopButton.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
});

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.needs-validation');
    
    if (forms.length > 0) {
        Array.from(forms).forEach(form => {
            form.addEventListener('submit', function(event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }
});

// Add active class to current page link
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (currentPath === '/' && href === '/')) {
            link.classList.add('active');
        }
    });
}); 