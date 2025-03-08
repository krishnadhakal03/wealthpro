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

function toggleMenu() {
    const menuItems = document.getElementById('menu-items');
    menuItems.classList.toggle('active');
}


