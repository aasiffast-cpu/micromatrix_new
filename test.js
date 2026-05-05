
// =====================
// WELCOME TEXT ANIMATION
// =====================

function easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
}

function animateSlideIn(element, startX, duration, delay) {
    if (!element) return;
    const startTime = performance.now() + delay;

    function step(currentTime) {
        if (currentTime < startTime) {
            requestAnimationFrame(step);
            return;
        }
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = easeOutCubic(progress);
        const currentX = startX * (1 - eased);
        element.style.transform = 'translateX(' + currentX + '%)';
        if (progress < 1) {
            requestAnimationFrame(step);
        }
    }
    requestAnimationFrame(step);
}

document.addEventListener('DOMContentLoaded', function() {
    const welcomeText = document.getElementById('welcome-text');
    const micromatrixText = document.getElementById('micromatrix-text');
    // Simple fade-in instead of slide from outside to avoid clipping
    if(micromatrixText) {
        micromatrixText.style.opacity = '0';
        micromatrixText.style.transform = 'scale(0.8)';
        micromatrixText.style.transition = 'all 0.8s ease';
        setTimeout(() => {
            micromatrixText.style.opacity = '1';
            micromatrixText.style.transform = 'scale(1)';
        }, 300);
    }
});

// =====================
// NAVIGATION TOGGLE
// =====================

function toggleMenu() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    const menuToggle = document.getElementById('menuToggle');
    
    sidebar.classList.toggle('open');
    overlay.classList.toggle('active');
    menuToggle.classList.toggle('open');
}

document.querySelectorAll('.sidebar-link').forEach(link => {
    link.addEventListener('click', () => {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebarOverlay');
        const menuToggle = document.getElementById('menuToggle');
        sidebar.classList.remove('open');
        overlay.classList.remove('active');
        menuToggle.classList.remove('open');
    });
});

document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebarOverlay');
        const menuToggle = document.getElementById('menuToggle');
        sidebar.classList.remove('open');
        overlay.classList.remove('active');
        menuToggle.classList.remove('open');
    });
});

// =====================
// SERVICE CARD INTERACTIONS
// =====================

let currentActiveCard = null;

function showSubcategories(element) {
    const dropdown = element.querySelector('.subcategories-dropdown');
    if (dropdown) {
        dropdown.style.display = 'flex';
        dropdown.style.animation = 'slideIn 0.3s ease forwards';
        element.classList.add('active-service');
    }
}

function hideSubcategories(element) {
    const dropdown = element.querySelector('.subcategories-dropdown');
    if (dropdown) {
        dropdown.style.display = 'none';
        element.classList.remove('active-service');
    }
}

// Service Card Click Handler
document.addEventListener('DOMContentLoaded', function() {
    const serviceCards = document.querySelectorAll('.service-card');
    
    serviceCards.forEach(card => {
        // Click handler
        card.addEventListener('click', function(e) {
            if (e.target.closest('.subcategories-dropdown')) {
                return;
            }
            
            // Close other cards
            if (currentActiveCard && currentActiveCard !== card) {
                hideSubcategories(currentActiveCard);
            }
            
            // Toggle current card
            const dropdown = card.querySelector('.subcategories-dropdown');
            if (dropdown && dropdown.style.display === 'none') {
                showSubcategories(card);
                currentActiveCard = card;
            } else {
                hideSubcategories(card);
                currentActiveCard = null;
            }
        });
        
        // Hover handlers for visual feedback
        card.addEventListener('mouseenter', function() {
            if (currentActiveCard !== this) {
                this.style.transform = 'translateY(-8px)';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            if (currentActiveCard !== this) {
                this.style.transform = 'translateY(0)';
            }
        });
        
        // Prevent dropdown from closing on internal click
        const dropdown = card.querySelector('.subcategories-dropdown');
        if (dropdown) {
            dropdown.addEventListener('click', function(e) {
                e.stopPropagation();
            });
        }
    });
});

// =====================
// SCROLL TO SECTION
// =====================

function scrollToContact() {
    const contactSection = document.querySelector('.contact-section') || document.querySelector('.cta-section');
    if (contactSection) {
        contactSection.scrollIntoView({ behavior: 'smooth' });
    } else {
        window.location.href = '/contact';
    }
}

// =====================
// SCROLL ANIMATIONS
// =====================

const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeIn 0.6s ease forwards';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.overview-card, .review-card, .service-card, .info-card, .detail-card, .stat-card, .showcase-service').forEach(card => {
        observer.observe(card);
    });
});

// =====================
// CHATBOT FUNCTIONALITY - FIXED
// =====================

let chatbotOpen = false;

function toggleChatbot() {
    const widget = document.getElementById('chatbotWidget');
    const toggle = document.querySelector('.chatbot-toggle');
    
    if (widget) {
        chatbotOpen = !chatbotOpen;
        if (chatbotOpen) {
            widget.classList.add('active');
            widget.style.display = 'flex';
            widget.style.flexDirection = 'column';
            widget.style.visibility = 'visible';
            widget.style.opacity = '1';
        } else {
            widget.classList.remove('active');
            widget.style.opacity = '0';
            setTimeout(() => {
                widget.style.display = 'none';
                widget.style.visibility = 'hidden';
            }, 300);
        }
    }
}

function sendChatbotMessage() {
    const input = document.getElementById('chatbotInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    const messagesDiv = document.getElementById('chatbotMessages');
    
    // Add user message
    const userMsg = document.createElement('div');
    userMsg.className = 'chatbot-message user-message';
    userMsg.innerHTML = '<p>' + escapeHtml(message) + '</p>';
    messagesDiv.appendChild(userMsg);
    
    input.value = '';
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    // Add loading indicator
    const loadingMsg = document.createElement('div');
    loadingMsg.className = 'chatbot-message bot-message loading';
    loadingMsg.innerHTML = '<p>⏳ Thinking...</p>';
    messagesDiv.appendChild(loadingMsg);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    // Send to server
    fetch('/api/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        // Remove loading message
        loadingMsg.remove();
        
        // Add bot response
        const botMsg = document.createElement('div');
        botMsg.className = 'chatbot-message bot-message';
        botMsg.innerHTML = '<p>' + escapeHtml(data.response) + '</p>';
        botMsg.style.animation = 'slideIn 0.3s ease forwards';
        messagesDiv.appendChild(botMsg);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    })
    .catch(error => {
        console.error('Chatbot error:', error);
        loadingMsg.remove();
        
        const errorMsg = document.createElement('div');
        errorMsg.className = 'chatbot-message bot-message';
        errorMsg.innerHTML = '<p>Sorry, I encountered an error. Please try again.</p>';
        messagesDiv.appendChild(errorMsg);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    });
}

function handleChatbotKeypress(event) {
    if (event.key === 'Enter') {
        sendChatbotMessage();
    }
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Initialize chatbot on page load
document.addEventListener('DOMContentLoaded', function() {
    const chatbotWidget = document.getElementById('chatbotWidget');
    if (chatbotWidget) {
        chatbotWidget.style.display = 'none';
        chatbotWidget.style.visibility = 'hidden';
        chatbotWidget.style.opacity = '0';
        chatbotWidget.style.transition = 'opacity 0.3s ease';
    }
});

// =====================
// CONTACT FORM
// =====================

function handleContactForm(event) {
    event.preventDefault();
    
    const formData = new FormData(document.getElementById('contactForm'));
    const messageDiv = document.getElementById('formMessage');
    const submitBtn = document.querySelector('.submit-btn');
    
    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending...';
    
    fetch('/contact', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            messageDiv.textContent = '✓ Thank you! We will contact you within 24 hours.';
            messageDiv.className = 'form-message success';
            messageDiv.style.display = 'block';
            document.getElementById('contactForm').reset();
            submitBtn.textContent = 'Send Message';
            submitBtn.disabled = false;
            
            setTimeout(() => {
                messageDiv.style.display = 'none';
            }, 5000);
        }
    })
    .catch(error => {
        console.error('Form error:', error);
        messageDiv.textContent = '✓ Thank you! We will contact you within 24 hours.';
        messageDiv.className = 'form-message success';
        messageDiv.style.display = 'block';
        submitBtn.textContent = 'Send Message';
        submitBtn.disabled = false;
    });
}

// =====================
// PAGE LOAD ANIMATIONS
// =====================

window.addEventListener('load', () => {
    // Stagger animations for hero elements
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        const elements = heroSection.querySelectorAll('h1, p, .hero-actions, .hero-highlights');
        elements.forEach((el, index) => {
            el.style.animation = 'fadeInUp 0.8s ease forwards';
            el.style.animationDelay = (index * 0.1) + 's';
        });
    }
});

// =====================
// UTILITY FUNCTIONS
// =====================

// Smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#') {
            e.preventDefault();
            const element = document.querySelector(href);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth' });
            }
        }
    });
});

// Add active state to nav links based on scroll position
window.addEventListener('scroll', () => {
    const scrollPosition = window.scrollY;
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
});

// Close mobile menu on window resize
window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
        const navbar = document.getElementById('navbar');
        const menuToggle = document.getElementById('menuToggle');
        if (navbar) navbar.classList.remove('active');
    }
});

// =====================
// NEW ANIMATIONS & EFFECTS
// =====================

// 1. Scroll Progress Bar
document.addEventListener('scroll', function() {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    let bar = document.getElementById('scroll-progress-bar');
    if(!bar) {
        bar = document.createElement('div');
        bar.id = 'scroll-progress-bar';
        document.body.appendChild(bar);
    }
    bar.style.width = scrolled + '%';
});

// 2. Ripple Effect on Buttons
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.cta-button, .cta-button-large, .package-btn, .submit-btn');
    buttons.forEach(btn => {
        btn.classList.add('ripple-btn');
        btn.addEventListener('click', function(e) {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const circle = document.createElement('span');
            circle.classList.add('ripple');
            circle.style.left = `${x}px`;
            circle.style.top = `${y}px`;
            
            this.appendChild(circle);
            setTimeout(() => circle.remove(), 600);
        });
    });
});

// 3. 3D Tilt Effect on Cards
document.addEventListener('DOMContentLoaded', function() {
    const tiltCards = document.querySelectorAll('.overview-card, .review-card, .service-card');
    tiltCards.forEach(card => {
        card.addEventListener('mousemove', e => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = ((y - centerY) / centerY) * -10;
            const rotateY = ((x - centerX) / centerX) * 10;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
            card.style.transition = 'none';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
            card.style.transition = 'transform 0.5s ease';
        });
    });
});

// 4. Animated Number Counters
document.addEventListener('DOMContentLoaded', function() {
    const counters = document.querySelectorAll('.stat-card h3');
    const counterObserver = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const text = target.innerText;
                const targetNumber = parseInt(text.replace(/[^0-9]/g, ''));
                if (!isNaN(targetNumber)) {
                    let count = 0;
                    const duration = 2000;
                    const increment = targetNumber / (duration / 16);
                    
                    const updateCount = () => {
                        count += increment;
                        if (count < targetNumber) {
                            target.innerText = Math.ceil(count) + text.replace(/[0-9]/g, '');
                            requestAnimationFrame(updateCount);
                        } else {
                            target.innerText = text;
                        }
                    };
                    updateCount();
                }
                obs.unobserve(target);
            }
        });
    }, { threshold: 0.5 });
    
    counters.forEach(counter => counterObserver.observe(counter));
});

// 5. Typing Effect for Hero Subtitle
document.addEventListener('DOMContentLoaded', function() {
    const subtitle = document.querySelector('.hero-subtitle');
    if (subtitle) {
        const text = subtitle.innerText;
        subtitle.innerText = '';
        subtitle.style.minHeight = '1.6em'; // prevent layout shift
        let i = 0;
        function typeWriter() {
            if (i < text.length) {
                subtitle.innerHTML += text.charAt(i);
                i++;
                setTimeout(typeWriter, 50);
            }
        }
        setTimeout(typeWriter, 1000);
    }
});

// 6. Password Visibility Toggle
function togglePassword(inputId, button) {
    const input = document.getElementById(inputId);
    const icon = button.querySelector('i');
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}
