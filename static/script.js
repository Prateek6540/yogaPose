// Mobile Navigation
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        hamburger.classList.toggle('active');
    });
}

// Form handling for login
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const email = this.querySelector('input[type="email"]').value;
        const password = this.querySelector('input[type="password"]').value;
        
        // Here you would typically make an API call to your backend
        console.log('Login attempt:', { email, password });
        alert('Login functionality would be implemented with a backend service');
    });
}

// Form handling for registration
const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const fullname = this.querySelector('input[type="text"]').value;
        const email = this.querySelector('input[type="email"]').value;
        const password = this.querySelectorAll('input[type="password"]')[0].value;
        const confirmPassword = this.querySelectorAll('input[type="password"]')[1].value;

        // Basic validation
        if (password !== confirmPassword) {
            alert('Passwords do not match!');
            return;
        }

        // Here you would typically make an API call to your backend
        console.log('Registration attempt:', { fullname, email, password });
        alert('Registration functionality would be implemented with a backend service');
    });
}

// Contact form handling
const contactForm = document.querySelector('.contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const name = this.querySelector('input[type="text"]').value;
        const email = this.querySelector('input[type="email"]').value;
        const message = this.querySelector('textarea').value;

        // Here you would typically make an API call to your backend
        console.log('Contact form submission:', { name, email, message });
        alert('Thank you for your message! We will get back to you soon.');
        this.reset();
    });
}

// Booking form handling
const bookingForm = document.getElementById('bookingForm');
if (bookingForm) {
    bookingForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = {
            fullname: this.querySelector('#fullname').value,
            email: this.querySelector('#email').value,
            phone: this.querySelector('#phone').value,
            date: this.querySelector('#date').value,
            time: this.querySelector('#time').value,
            class: this.querySelector('#class').value,
            notes: this.querySelector('#notes').value
        };

        // Here you would typically make an API call to your backend
        console.log('Booking submission:', formData);
        
        // Show success message
        alert('Thank you for your booking! We will confirm your reservation shortly.');
        this.reset();
    });

    // Set minimum date to today
    const dateInput = bookingForm.querySelector('#date');
    const today = new Date().toISOString().split('T')[0];
    dateInput.min = today;
}

// Smooth scrolling for all anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar scroll effect
const navbar = document.querySelector('.navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll <= 0) {
        navbar.classList.remove('scroll-up');
        return;
    }
    
    if (currentScroll > lastScroll && !navbar.classList.contains('scroll-down')) {
        // Scroll Down
        navbar.classList.remove('scroll-up');
        navbar.classList.add('scroll-down');
    } else if (currentScroll < lastScroll && navbar.classList.contains('scroll-down')) {
        // Scroll Up
        navbar.classList.remove('scroll-down');
        navbar.classList.add('scroll-up');
    }
    lastScroll = currentScroll;
});

// Add animation to elements when they come into view
const animateOnScroll = () => {
    const elements = document.querySelectorAll('.class-card, .feature, .contact-form, .contact-info');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    elements.forEach(element => {
        observer.observe(element);
    });
};

// Class filtering functionality
const initClassFilters = () => {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const classCards = document.querySelectorAll('.class-card');

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            button.classList.add('active');

            const filter = button.getAttribute('data-filter');

            classCards.forEach(card => {
                if (filter === 'all' || card.getAttribute('data-level') === filter) {
                    card.style.display = 'block';
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, 100);
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px)';
                    setTimeout(() => {
                        card.style.display = 'none';
                    }, 300);
                }
            });
        });
    });
};

// Initialize all functionality
document.addEventListener('DOMContentLoaded', () => {
    animateOnScroll();
    initClassFilters();

    const isLoggedIn = localStorage.getItem('logged_in') === 'true';
    const body = document.body;

    if (!isLoggedIn) {
        body.classList.add('no-scroll');
        // Optionally, you might want to display a message or modal prompting login
        console.log('User not logged in. Scrolling disabled.');
    } else {
        body.classList.remove('no-scroll');
        console.log('User logged in. Scrolling enabled.');
    }
});

// For demonstration: Simulate login status toggle (remove in production)
// To test logged in state: run localStorage.setItem('logged_in', 'true'); location.reload(); in console
// To test logged out state: run localStorage.setItem('logged_in', 'false'); location.reload(); in console
// Or simply clear localStorage to revert to default (logged out) 