"""
MICROMATRIX - COMPLETE APPLICATION IN ONE FILE
All backend, frontend, HTML, CSS, and JavaScript combined into a single Python file
Flask Application with Embedded Templates and Assets
"""

from flask import Flask, render_template_string, request, jsonify, redirect, url_for
from flask_mail import Mail, Message
from datetime import datetime
import os

app = Flask(__name__)

# =====================
# CONFIGURATION
# =====================
app.config['SECRET_KEY'] = "micromatrix_secret_key_2026"
app.config['DEBUG'] = True

# Email Configuration
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', True)
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'info@micromatrix.tech')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'info@micromatrix.tech')

mail = Mail(app)

OWNER_EMAIL = 'info@micromatrix.tech'
OWNER_NAME = 'Muhammad Asif - Micromatrix'

# =====================
# DATA STRUCTURES
# =====================

reviews = [
    {'name': 'Ahmed Hassan', 'company': 'Tech Solutions Inc', 'rating': 5, 'text': 'Micromatrix delivered an outstanding ERP system for our company. Professional team and excellent support!', 'image': '👤'},
    {'name': 'Fatima Khan', 'company': 'E-Commerce Hub', 'rating': 5, 'text': 'The e-commerce website they developed increased our sales by 150%. Highly recommended!', 'image': '👤'},
    {'name': 'Muhammad Ali', 'company': 'Digital Marketing Pro', 'rating': 4.8, 'text': 'Great mobile app development team. They delivered on time and within budget.', 'image': '👤'},
    {'name': 'Sarah Johnson', 'company': 'Finance Corp', 'rating': 5, 'text': 'Their fintech solutions are cutting edge. Very professional and innovative team.', 'image': '👤'},
    {'name': 'Rizwan Sheikh', 'company': 'AI StartUp', 'rating': 4.9, 'text': 'The AI and machine learning solutions transformed our business processes.', 'image': '👤'}
]

chatbot_knowledge = {
    'who are you': "I'm the Micromatrix Assistant. I'm here to help you with information about our company, services, and how we can help your business.",
    'what is micromatrix': 'Micromatrix is an innovative technology company specializing in custom software solutions, web development, mobile apps, AI/ML, cloud services, and much more. We have a remote-first team dedicated to delivering excellence.',
    'what services do you offer': 'We offer 15 comprehensive services including: Software Development, Web Development, Mobile App Development, AI & Machine Learning, Cloud Computing, Data Science, E-Commerce Solutions, Digital Marketing, Software Testing, IT Consulting, Fintech Solutions, ERP Systems, Game Development, UI/UX Design, and Emerging Technologies.',
    'how can i contact you': 'You can reach us at: Phone: +923316170980 | WhatsApp: https://wa.me/923316170980 | Email: info@micromatrix.tech. We provide 24/7 support for all inquiries.',
    'what is your phone': 'Our phone number is +923316170980. Call us anytime!',
    'what is your email': 'Our email is info@micromatrix.tech. We respond to emails within 24 hours.',
    'are you a remote company': 'Yes! Micromatrix is a remote-first company. This allows us to serve clients globally with flexibility and efficiency.',
    'do you provide support': 'Absolutely! We provide 24/7 support to all our clients. Our team is always available to assist you.',
    'what is your location': 'Micromatrix is a remote-first company with a global team. We serve clients worldwide without geographical limitations.',
    'can you help with my project': 'Yes! We can definitely help. Tell us about your project needs and we can provide a custom solution. Contact our team or fill out our contact form.',
    'do you have experience': 'Yes, we have extensive experience across multiple industries and have successfully completed numerous projects for satisfied clients.',
    'what technology do you use': 'We use cutting-edge technologies including: React, Angular, Node.js, Python, Django, Flutter, AWS, Azure, Docker, Kubernetes, TensorFlow, and many more.',
    'hello': 'Hello! Welcome to Micromatrix. How can I help you today?',
    'hi': "Hi there! I'm the Micromatrix Assistant. Feel free to ask me anything about our services or company.",
    'help': 'I can help you with information about Micromatrix services, pricing, contact details, or any questions about our company. What would you like to know?',
    'thanks': "You're welcome! Feel free to ask me anything else about Micromatrix.",
    'thank you': "My pleasure! Is there anything else you'd like to know?"
}

services_data = {
    'Software Development': {'icon': '💻', 'description': 'Complete software solutions tailored to your business needs', 'subcategories': ['Custom Software Development', 'Enterprise Software (ERP systems)', 'CRM (Customer Relationship Management Systems)', 'Desktop Applications']},
    'Web Development': {'icon': '🌐', 'description': 'Modern web solutions for your online presence', 'subcategories': ['Website Design (UI/UX)', 'Frontend + Backend Development', 'E-commerce websites (Shopify, WooCommerce)', 'CMS (WordPress, Joomla)']},
    'Mobile App Development': {'icon': '📱', 'description': 'High-performance mobile applications', 'subcategories': ['Android App Development', 'iOS App Development', 'Cross-platform apps (Flutter, React Native)']},
    'Artificial Intelligence (AI) & Machine Learning': {'icon': '🤖', 'description': 'AI-powered solutions for modern businesses', 'subcategories': ['Chatbots', 'Automation systems', 'Data prediction models', 'Computer vision']},
    'Cloud Computing Services': {'icon': '☁️', 'description': 'Scalable cloud infrastructure solutions', 'subcategories': ['Cloud hosting (AWS, Azure)', 'Cloud migration', 'SaaS solutions']},
    'Data Science & Analytics': {'icon': '📊', 'description': 'Transform data into actionable insights', 'subcategories': ['Data analysis', 'Business intelligence', 'Big data solutions']},
    'E-Commerce Solutions': {'icon': '🛍️', 'description': 'Complete online store solutions', 'subcategories': ['Online store development', 'Payment gateway integration', 'Inventory systems']},
    'Digital Marketing Services': {'icon': '📢', 'description': 'Drive your online visibility and growth', 'subcategories': ['SEO (Search Engine Optimization)', 'Social Media Marketing', 'Google Ads / PPC', 'Content writing']},
    'Software Testing & QA': {'icon': '✅', 'description': 'Ensure quality and reliability', 'subcategories': ['Manual testing', 'Automation testing', 'Performance testing']},
    'IT Consulting & Support': {'icon': '🔧', 'description': 'Expert IT guidance and support', 'subcategories': ['Business IT consultancy', 'Technical support', 'System integration']},
    'Fintech & Banking Solutions': {'icon': '💳', 'description': 'Secure financial technology solutions', 'subcategories': ['Digital banking apps', 'Payment systems', 'Leasing/finance software']},
    'ERP & Business Automation': {'icon': '⚙️', 'description': 'Automate and optimize business processes', 'subcategories': ['HR systems', 'Inventory systems', 'Accounting software']},
    'Game Development': {'icon': '🎮', 'description': 'Create engaging gaming experiences', 'subcategories': ['Mobile games', 'PC games', 'Unity / Unreal Engine projects']},
    'UI/UX Design Services': {'icon': '🎨', 'description': 'Beautiful and intuitive user interfaces', 'subcategories': ['App design', 'Website interface design', 'User experience optimization']},
    'Emerging Technologies': {'icon': '🚀', 'description': 'Future-ready technology solutions', 'subcategories': ['Blockchain development', 'IoT (Internet of Things)', 'AR/VR apps']}
}

pricing_data = {
    "tiers": [
        {
            "name": "Starter",
            "range": "$100 - $500",
            "features": ["✓ Single Service", "✓ 1-2 weeks delivery", "✓ Basic Support", "✓ 1 Revision Round"],
            "badge": "Most Affordable",
            "color": "#10b981"
        },
        {
            "name": "Basic",
            "range": "$500 - $1,000",
            "features": ["✓ 2-3 Services", "✓ 2-4 weeks delivery", "✓ Standard Support", "✓ 3 Revision Rounds", "✓ Basic Analytics"],
            "badge": "Most Popular",
            "color": "#3b82f6"
        },
        {
            "name": "Professional",
            "range": "$1,000 - $2,000",
            "features": ["✓ Multiple Services", "✓ 1-3 months", "✓ Priority Support 24/7", "✓ Unlimited Revisions", "✓ Dedicated Manager", "✓ Advanced Analytics"],
            "badge": "Premium",
            "color": "#8b5cf6"
        }
    ],
    "budget_options": [
        "$100 - $500", "$2,000 - $3,000", "$1,000 - $2,000", "$2,000 - $5,000",
        "$5,000 - $10,000", "$10,000+"
    ]
}

# =====================
# HTML TEMPLATES
# =====================

BASE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Micromatrix{% endblock %}</title>
    <style>
        {{ css_content }}
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="header-container">
            <div class="logo-header">
                <div class="company-info">
                    <h1>MICROMATRIX</h1>
                    <p>INNOVATIVE</p>
                </div>
            </div>
            
            <!-- Toggle Menu Button -->
            <button class="menu-toggle" id="menuToggle" onclick="toggleMenu()">
                <span></span>
                <span></span>
                <span></span>
            </button>

            <!-- Navigation -->
            <nav class="navbar" id="navbar">
                <a href="/home" class="nav-link">Home</a>
                <a href="/about" class="nav-link">About</a>
                <a href="/services" class="nav-link">Services</a>
                <a href="/contact" class="nav-link">Contact Us</a>
            </nav>
        </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="footer-content">
            <div class="footer-section">
                <h3>Micromatrix</h3>
                <p>Leading provider of innovative technology solutions</p>
                <p class="tagline-small">Remote-First Company</p>
            </div>

            <div class="footer-section">
                <h4>Contact Information</h4>
                <p>📞 Phone: +923316170980</p>
                <p>📞 Personal: +92 3039977330</p>
                <p>💬 WhatsApp: <a href="https://wa.me/923316170980" target="_blank" class="footer-link">+923316170980</a></p>
                <p>📧 Email: info@micromatrix.tech</p>
                <p>🌍 Service: Global Remote Services</p>
            </div>

            <div class="footer-section">
                <h4>Quick Links</h4>
                <ul>
                    <li><a href="/home">Home</a></li>
                    <li><a href="/about">About</a></li>
                    <li><a href="/services">Services</a></li>
                    <li><a href="/contact">Contact</a></li>
                </ul>
            </div>

            <div class="footer-section">
                <h4>Company Stats</h4>
                <p>✓ 100+ Projects Delivered</p>
                <p>✓ Remote Team</p>
                <p>✓ 15 Service Categories</p>
            </div>
        </div>

        <div class="footer-bottom">
            <p>&copy; 2026 Micromatrix. All rights reserved. | Innovative Solutions for Modern Businesses</p>
        </div>
    </footer>

    <!-- Chatbot Widget -->
    <div class="chatbot-widget" id="chatbotWidget">
        <div class="chatbot-header">
            <h3>Micromatrix Assistant</h3>
            <button class="chatbot-close" onclick="toggleChatbot()">✕</button>
        </div>
        <div class="chatbot-messages" id="chatbotMessages">
            <div class="chatbot-message bot-message">
                <p>Hi! 👋 I'm the Micromatrix Assistant. Ask me anything about our services, contact info, or company!</p>
            </div>
        </div>
        <div class="chatbot-input-area">
            <input 
                type="text" 
                id="chatbotInput" 
                placeholder="Ask me something..." 
                onkeypress="handleChatbotKeypress(event)"
                class="chatbot-input"
            >
            <button onclick="sendChatbotMessage()" class="chatbot-send">Send</button>
        </div>
    </div>

    <!-- Chatbot Toggle Button -->
    <button class="chatbot-toggle" onclick="toggleChatbot()" title="Chat with us">
        💬
    </button>

    <script>
        {{ js_content }}
    </script>
    {% block scripts %}{% endblock %}
</body>
</html>
"""

HOME_TEMPLATE = """
<div class="hero-section">
    <div class="home-hero-grid">
        <div class="hero-content hero-content-wide">
<div class="hero-badge">Welcome to Micromatrix</div>
            <div class="hero-title-container">
                <h1><span id="micromatrix-text">Micromatrix</span></h1>
            </div>
            <p class="hero-subtitle">Your Partner in Digital Innovation</p>
            <p class="hero-description">Transforming businesses through cutting-edge technology solutions with premium design, AI, cloud services, and enterprise-grade software.</p>
            <div class="hero-actions">
                <a href="/services" class="cta-button">Explore Our Services</a>
                <a href="/contact" class="cta-button secondary">Request Consultation</a>
            </div>
            <div class="hero-highlights">
                <div>
                    <h4>15 Expert Services</h4>
                    <p>From software to AI, cloud, fintech and custom automation.</p>
                </div>
                <div>
                    <h4>Remote Global Team</h4>
                    <p>Delivered by a distributed team with modern collaboration.</p>
                </div>
                <div>
                    <h4>Quality First</h4>
                    <p>Designed for trust, performance, and long-term success.</p>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Company Overview -->
<section class="company-overview">
    <h2>About Micromatrix</h2>
    <div class="overview-grid">
        <div class="overview-card">
            <div class="card-icon">🌍</div>
            <h3>Global Remote Company</h3>
            <p>Operating worldwide with a distributed team of talented professionals</p>
        </div>
        <div class="overview-card">
            <div class="card-icon">⚡</div>
            <h3>Fast & Reliable</h3>
            <p>Quick turnaround times without compromising on quality</p>
        </div>
        <div class="overview-card">
            <div class="card-icon">🔒</div>
            <h3>Secure Solutions</h3>
            <p>Enterprise-grade security for all our services and projects</p>
        </div>
        <div class="overview-card">
            <div class="card-icon">🚀</div>
            <h3>Innovation Focused</h3>
            <p>Always using the latest technologies for modern solutions</p>
        </div>
    </div>
</section>

<!-- Customer Reviews & Ratings -->
<section id="review-section" class="reviews-section">
    <h2>Customer Reviews & Ratings</h2>
    <div class="reviews-container">
        {% for review in reviews %}
        <div class="review-card">
            <div class="review-header">
                <div class="reviewer-info">
                    <div class="avatar">{{ review.image }}</div>
                    <div>
                        <h4>{{ review.name }}</h4>
                        <p class="company">{{ review.company }}</p>
                    </div>
                </div>
                <div class="rating">
                    <span class="stars">
                        {% if review.rating >= 5 %}⭐⭐⭐⭐⭐{% elif review.rating >= 4 %}⭐⭐⭐⭐{% elif review.rating >= 3 %}⭐⭐⭐{% elif review.rating >= 2 %}⭐⭐{% else %}⭐{% endif %}
                    </span>
                    <span class="rating-value">{{ review.rating }}/5</span>
                </div>
            </div>
            <p class="review-text">"{{ review.text }}"</p>
        </div>
        {% endfor %}
    </div>

    <div class="average-rating">
        <h3>Overall Rating</h3>
        <div class="rating-display">
            <span class="big-rating">4.9</span>
            <span class="out-of">/5.0</span>
        </div>
        <p>Based on customer reviews</p>
    </div>
</section>

<!-- Quick Stats -->
<section class="stats-section">
    <div class="stat-card">
        <h3>100+</h3>
        <p>Projects Delivered</p>
    </div>
    <div class="stat-card">
        <h3>15</h3>
        <p>Service Categories</p>
    </div>
    <div class="stat-card">
        <h3>24/7</h3>
        <p>Support Available</p>
    </div>
    <div class="stat-card">
        <h3>∞</h3>
        <p>Global Reach</p>
    </div>
</section>

<!-- Services Showcase Section -->
<section id="services-highlights" class="services-showcase">
    <div class="showcase-header">
        <h2>🌟 Our Comprehensive Services</h2>
        <p>15 Specialized Technology Solutions for Your Business</p>
    </div>
    <div class="showcase-grid">
        <div class="showcase-service">
            <div class="showcase-icon">💻</div>
            <h4>Software Development</h4>
            <p>Custom & Enterprise Solutions</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon">🌐</div>
            <h4>Web Development</h4>
            <p>Modern Web Solutions</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon">📱</div>
            <h4>Mobile App Development</h4>
            <p>iOS, Android & Cross-Platform</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon">🤖</div>
            <h4>AI & Machine Learning</h4>
            <p>Intelligent Automation</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon">☁️</div>
            <h4>Cloud Computing</h4>
            <p>AWS, Azure & SaaS</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon">📊</div>
            <h4>Data Science</h4>
            <p>Analytics & Business Intelligence</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon">🛍️</div>
            <h4>E-Commerce Solutions</h4>
            <p>Complete Online Stores</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon">📢</div>
            <h4>Digital Marketing</h4>
            <p>SEO, Social Media & Ads</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon">✅</div>
            <h4>Software Testing & QA</h4>
            <p>Quality Assurance</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon">🔧</div>
            <h4>IT Consulting</h4>
            <p>Expert Guidance & Support</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon">💳</div>
            <h4>Fintech Solutions</h4>
            <p>Banking & Payment Systems</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon">⚙️</div>
            <h4>ERP & Automation</h4>
            <p>Business Process Automation</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon">🎮</div>
            <h4>Game Development</h4>
            <p>Mobile & PC Games</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon">🎨</div>
            <h4>UI/UX Design</h4>
            <p>User Interface & Experience</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon">🚀</div>
            <h4>Emerging Technologies</h4>
            <p>Blockchain, IoT & AR/VR</p>
        </div>
    </div>
    <div class="showcase-cta">
        <a href="/services" class="cta-button">Explore All Services →</a>
    </div>
</section>

<!-- Call to Action -->
<section class="cta-section">
    <h2>Ready to Transform Your Business?</h2>
    <p>Let's discuss your project and explore how Micromatrix can help you achieve your goals</p>
    <a href="/contact" class="cta-button-large">Contact Us Today</a>
</section>

"""

SERVICES_TEMPLATE = """
<div class="services-hero">
    <h1>Our Services</h1>
    <p>Comprehensive technology solutions tailored to your business needs</p>
</div>

<section class="services-main">
    <div class="services-container">
        {% for service_name, service_data in services.items() %}
        <div class="service-card" onmouseover="showSubcategories(this)" onmouseout="hideSubcategories(this)">
            <div class="service-main">
                <div class="service-icon">{{ service_data.icon }}</div>
                <h3>{{ service_name }}</h3>
                <p class="service-description">{{ service_data.description }}</p>
                <span class="hover-hint">Hover to see details →</span>
            </div>

            <!-- Subcategories (Hidden by default, shown on hover) -->
            <div class="subcategories-dropdown">
                <div class="subcategories-header">
                    <h4>{{ service_name }}</h4>
                </div>
                <ul class="subcategories-list">
                    {% for subcategory in service_data.subcategories %}
                    <li class="subcategory-item">
                        <span class="checkbox">✓</span>
                        {{ subcategory }}
                    </li>
                    {% endfor %}
                </ul>
                <div class="subcategories-action">
                    <button class="inquiry-btn" onclick="scrollToContact()">Inquire Now</button>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</section>

<!-- Services Details Section -->
<section class="services-details">
    <h2>Why Choose Micromatrix?</h2>
    <div class="details-grid">
        <div class="detail-card">
            <div class="detail-icon">🎯</div>
            <h4>Focused Solutions</h4>
            <p>Each service is carefully crafted with specific business needs in mind</p>
        </div>
        <div class="detail-card">
            <div class="detail-icon">⚡</div>
            <h4>Fast Delivery</h4>
            <p>Quick implementation without compromising on quality standards</p>
        </div>
        <div class="detail-card">
            <div class="detail-icon">💡</div>
            <h4>Innovation</h4>
            <p>Latest technologies and best practices to keep you ahead</p>
        </div>
        <div class="detail-card">
            <div class="detail-icon">🔧</div>
            <h4>Expert Team</h4>
            <p>Experienced professionals with proven track record</p>
        </div>
        <div class="detail-card">
            <div class="detail-icon">📈</div>
            <h4>Results Driven</h4>
            <p>Focused on delivering measurable business outcomes</p>
        </div>
        <div class="detail-card">
            <div class="detail-icon">🌍</div>
            <h4>Global Support</h4>
            <p>24/7 support available from our distributed team</p>
        </div>
    </div>
</section>

<!-- Technology Stack -->
<section class="tech-stack">
    <h2>Our Technology Stack</h2>
    <div class="tech-grid">
        <div class="tech-category">
            <h4>Web Technologies</h4>
            <p>React, Angular, Vue.js, Node.js, Django, Flask</p>
        </div>
        <div class="tech-category">
            <h4>Mobile Development</h4>
            <p>Flutter, React Native, Swift, Kotlin</p>
        </div>
        <div class="tech-category">
            <h4>Cloud & DevOps</h4>
            <p>AWS, Azure, Google Cloud, Docker, Kubernetes</p>
        </div>
        <div class="tech-category">
            <h4>AI & Data</h4>
            <p>Python, TensorFlow, PyTorch, Scikit-learn, SQL</p>
        </div>
        <div class="tech-category">
            <h4>Databases</h4>
            <p>PostgreSQL, MongoDB, MySQL, Redis, Firebase</p>
        </div>
        <div class="tech-category">
            <h4>Tools & Frameworks</h4>
            <p>Git, Jenkins, OpenCV, Blockchain, IoT Solutions</p>
        </div>
    </div>
</section>

<!-- Package Plans -->
<section class="service-packages">
    <h2>Service Packages</h2>
    <div class="packages-container">
        {% for tier in pricing.tiers %}
        <div class="package {% if tier.badge == 'Most Popular' %}featured{% endif %}">
            {% if tier.badge %}
            <div class="badge">{{ tier.badge }}</div>
            {% endif %}
            <h3>{{ tier.name }}</h3>
            <p class="price">{{ tier.range }}</p>
            <ul class="features-list">
                {% for feature in tier.features %}
                <li>{{ feature }}</li>
                {% endfor %}
            </ul>
            <button class="package-btn {% if tier.badge == 'Most Popular' %}featured-btn{% endif %}">
                {% if tier.name == 'Professional' %}Get Quote{% else %}Get Started{% endif %}
            </button>
        </div>
        {% endfor %}
    </div>
</section>

"""

CONTACT_TEMPLATE = """
<div class="contact-hero">
    <h1>Contact Us</h1>
    <p>Get in touch with our team for any inquiries or service requests</p>
</div>

<section class="contact-section">
    <div class="contact-container">
        <!-- Contact Information -->
        <div class="contact-info">
            <h2>Get in Touch</h2>
            
            <div class="info-cards">
                <div class="info-card">
                    <div class="info-icon">📞</div>
                    <h4>Phone Number</h4>
                    <p>+923316170980</p>
                    <p class="subtext">Available 24/7</p>
                </div>

                <div class="info-card">                    
                    <div class="info-icon">📱</div>
                    <h4>Secondary Number</h4>
                    <p><a href="tel:+923039977330" class="contact-link">+92 3039977330</a></p>
                    <p class="subtext">Direct support</p>
                </div>

                <div class="info-card">                    
                    <div class="info-icon">💬</div>
                    <h4>WhatsApp</h4>
                    <p><a href="https://wa.me/923316170980" target="_blank" class="contact-link">+923316170980</a></p>
                    <p class="subtext">Quick chat support</p>
                </div>

                <div class="info-card">
                    <div class="info-icon">📧</div>
                    <h4>Email Address</h4>
                    <p>info@micromatrix.tech</p>
                    <p class="subtext">Response within 24 hours</p>
                </div>

                <div class="info-card">
                    <div class="info-icon">🌍</div>
                    <h4>Global Reach</h4>
                    <p>Remote-First Company</p>
                    <p class="subtext">Serving clients worldwide</p>
                </div>

                <div class="info-card">
                    <div class="info-icon">⏰</div>
                    <h4>Support Hours</h4>
                    <p>24/7 Available</p>
                    <p class="subtext">Always here for you</p>
                </div>
            </div>

            <!-- Company Information -->
            <div class="company-details">
                <h3>Company Information</h3>
                <p><strong>Company Name:</strong> Micromatrix Innovative Solutions</p>
                <p><strong>Type:</strong> Remote-First Technology Company</p>
                <p><strong>Customers:</strong> 15+ Satisfied Clients</p>
                <p><strong>Specialization:</strong> Full-Stack Technology Solutions</p>
            </div>
        </div>

        <!-- Contact Form -->
        <div class="contact-form-wrapper">
            <h2>Send us a Message</h2>
            <form id="contactForm" class="contact-form" onsubmit="handleContactForm(event)">
                <div class="form-group">
                    <label for="name">Full Name *</label>
                    <input 
                        type="text" 
                        id="name" 
                        name="name" 
                        placeholder="Your full name" 
                        required
                    >
                </div>

                <div class="form-group">
                    <label for="email">Email Address *</label>
                    <input 
                        type="email" 
                        id="email" 
                        name="email" 
                        placeholder="your.email@example.com" 
                        required
                    >
                </div>

                <div class="form-group">
                    <label for="phone">Phone Number</label>
                    <input 
                        type="tel" 
                        id="phone" 
                        name="phone" 
                        placeholder="+92-XXX-XXXXXXX"
                    >
                </div>

                <div class="form-group">
                    <label for="service">Service of Interest *</label>
                    <select id="service" name="service" required>
                        <option value="">Select a service</option>
                        <option value="Software Development">Software Development</option>
                        <option value="Web Development">Web Development</option>
                        <option value="Mobile App Development">Mobile App Development</option>
                        <option value="AI & Machine Learning">AI & Machine Learning</option>
                        <option value="Cloud Computing">Cloud Computing Services</option>
                        <option value="Data Science">Data Science & Analytics</option>
                        <option value="E-Commerce">E-Commerce Solutions</option>
                        <option value="Digital Marketing">Digital Marketing Services</option>
                        <option value="Software Testing">Software Testing & QA</option>
                        <option value="IT Consulting">IT Consulting & Support</option>
                        <option value="Fintech">Fintech & Banking Solutions</option>
                        <option value="ERP">ERP & Business Automation</option>
                        <option value="Game Development">Game Development</option>
                        <option value="UI/UX Design">UI/UX Design Services</option>
                        <option value="Emerging Tech">Emerging Technologies</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="budget">Budget Range</label>
                    <select id="budget" name="budget">
                        <option value="">Select budget range</option>
                        {% for option in pricing.budget_options %}
                        <option value="{{ option }}">{{ option }}</option>
                        {% endfor %}
                    </select>
                </div>

                <div class="form-group">
                    <label for="message">Message *</label>
                    <textarea 
                        id="message" 
                        name="message" 
                        placeholder="Tell us about your project or inquiry..." 
                        rows="6" 
                        required
                    ></textarea>
                </div>

                <div class="form-group checkbox">
                    <input 
                        type="checkbox" 
                        id="terms" 
                        name="terms" 
                        required
                    >
                    <label for="terms" class="checkbox-label">
                        I agree to the terms and conditions
                    </label>
                </div>

                <button type="submit" class="submit-btn">Send Message</button>
                <div id="formMessage" class="form-message"></div>
            </form>
        </div>
    </div>
</section>

<!-- FAQ Section -->
<section class="faq-section">
    <h2>Frequently Asked Questions</h2>
    <div class="faq-container">
        <div class="faq-item">
            <h4>What is your project timeline?</h4>
            <p>Our project timelines vary based on complexity. Typically, we start with detailed assessment and provide estimated timelines from weeks to months.</p>
        </div>
        <div class="faq-item">
            <h4>Do you provide ongoing support?</h4>
            <p>Yes! We offer 24/7 support for all projects. Additional support packages are available for long-term partnerships.</p>
        </div>
        <div class="faq-item">
            <h4>What industries do you serve?</h4>
            <p>We serve finance, e-commerce, healthcare, technology, and more. Our expertise spans multiple sectors.</p>
        </div>
        <div class="faq-item">
            <h4>How do you ensure project confidentiality?</h4>
            <p>We maintain strict confidentiality agreements (NDA) and implement enterprise-grade security measures.</p>
        </div>
        <div class="faq-item">
            <h4>What are your payment terms?</h4>
            <p>Payment terms are flexible based on project requirements. We typically work with milestone-based payments.</p>
        </div>
        <div class="faq-item">
            <h4>Can you start immediately?</h4>
            <p>Yes, we can start immediately upon contract finalization. Our remote team allows quick mobilization.</p>
        </div>
    </div>
</section>

<!-- Quick Contact Cards -->
<section class="quick-contact">
    <h2>Quick Contact Options</h2>
    <div class="quick-cards">
        <a href="tel:+923316170980" class="quick-card phone-card">
            <div class="quick-icon">📞</div>
            <h4>Call Us</h4>
            <p>+923316170980</p>
            <span class="quick-action">Click to call →</span>
        </a>

        <a href="mailto:info@micromatrix.tech" class="quick-card email-card">
            <div class="quick-icon">📧</div>
            <h4>Email Us</h4>
            <p>info@micromatrix.tech</p>
            <span class="quick-action">Click to email →</span>
        </a>

        <div class="quick-card chat-card">
            <div class="quick-icon">💬</div>
            <h4>Chat Support</h4>
            <p>Available 24/7</p>
            <span class="quick-action">Start chat →</span>
        </div>
    </div>
</section>

"""

ABOUT_TEMPLATE = """
<section class="about-hero">
    <div class="about-hero-content">
        <span class="hero-badge">About Us</span>
        <h1>Building World-Class Digital Solutions Since 2020</h1>
        <p class="hero-description">Micromatrix was founded on the belief that exceptional software engineering and dedicated support can transform businesses of all sizes.</p>
        <div class="hero-actions">
            <a href="/contact" class="cta-button">Get in Touch</a>
            <a href="/services" class="cta-button secondary">Explore Services</a>
        </div>
    </div>
</section>

<section class="about-section">
    <div class="section-header">
        <h2>Who We Are</h2>
        <p>Driven by passion for excellence, led by Muhammad Asif from Pakistan</p>
    </div>

    <div class="about-grid">
        <div class="about-card">
            <h3>Our Story</h3>
            <p>Founded in 2020, Micromatrix emerged from a vision to deliver world-class software solutions. We've evolved into a dynamic, remote-first organization trusted by 100+ clients globally.</p>
        </div>
        <div class="about-card">
            <h3>Our Mission</h3>
            <p>To empower businesses with innovative, scalable software solutions that drive digital transformation, enhance operational efficiency, and unlock new growth opportunities.</p>
        </div>
        <div class="about-card">
            <h3>Our Vision</h3>
            <p>To be the most trusted and preferred technology partner for businesses seeking world-class digital solutions. We aspire to set industry standards for innovation and reliability.</p>
        </div>
    </div>
</section>

<section class="about-section">
    <div class="section-header">
        <h2>Our Core Strengths</h2>
        <p>Excellence in every line of code</p>
    </div>

    <div class="about-grid">
        <div class="strength-card">
            <div class="strength-icon">💎</div>
            <h3>Exceptional Software Engineering</h3>
            <p>We develop software with uncompromising quality standards. Every project meets rigorous quality benchmarks and exceeds client expectations.</p>
        </div>
        <div class="strength-card">
            <div class="strength-icon">🎯</div>
            <h3>Full-Spectrum Solutions</h3>
            <p>From concept to deployment and ongoing support, we handle every aspect of software development with specialized professionals.</p>
        </div>
        <div class="strength-card">
            <div class="strength-icon">🚀</div>
            <h3>Innovation & Agility</h3>
            <p>We stay at the forefront of technology trends, leveraging cutting-edge frameworks and cloud platforms with agile methodology.</p>
        </div>
    </div>
</section>

<section class="about-section">
    <div class="section-header">
        <h2>Our Promise to You</h2>
        <p>Excellence, reliability, and your success</p>
    </div>

    <div class="promise-grid">
        <div class="promise-card">
            <h3>✓ Quality Excellence</h3>
            <p>Every deliverable meets the highest industry standards through rigorous testing and quality assurance.</p>
        </div>
        <div class="promise-card">
            <h3>✓ Transparent Communication</h3>
            <p>Weekly updates and clear progress reports. You'll always know where your project stands.</p>
        </div>
        <div class="promise-card">
            <h3>✓ Timely Delivery</h3>
            <p>We respect your timelines and deliver on schedule using proven project management methodology.</p>
        </div>
        <div class="promise-card">
            <h3>✓ Scalable Solutions</h3>
            <p>Your software grows with your business. We design for scalability from day one.</p>
        </div>
        <div class="promise-card">
            <h3>✓ Security & Compliance</h3>
            <p>Enterprise-grade security and global compliance standards to safeguard your sensitive information.</p>
        </div>
        <div class="promise-card">
            <h3>✓ 24/7 Support</h3>
            <p>Continuous monitoring, maintenance, and technical support to keep your systems running smoothly.</p>
        </div>
    </div>
</section>

<section class="about-cta">
    <h2>Ready to Transform Your Business?</h2>
    <p>Let's collaborate and build something extraordinary together</p>
    <div class="cta-actions">
        <a href="/contact" class="cta-button">Start Your Project Today</a>
        <a href="tel:+923316170980" class="cta-button secondary">Call Us Now</a>
    </div>
</section>
"""

# =====================
# CSS CONTENT
# =====================

CSS_CONTENT = """
:root {
    --navy-primary: #001a4d;
    --navy-dark: #000d26;
    --navy-light: #003399;
    --white-primary: #ffffff;
    --white-secondary: #f8f9fa;
    --accent-purple: #7c3aed;
    --accent-blue: #3b82f6;
    --text-dark: #1a1a1a;
    --text-light: #666666;
    --border-color: #e5e7eb;
    --success-color: #10b981;
    --error-color: #ef4444;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--white-primary);
    color: var(--text-dark);
    line-height: 1.6;
}

.header {
    background: var(--navy-primary);
    color: var(--white-primary);
    padding: 1rem 2rem;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
}

.header-container {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    cursor: pointer;
}

.company-info h1 {
    font-size: 1.5rem;
    margin: 0;
    letter-spacing: 1px;
}

.company-info p {
    font-size: 0.75rem;
    margin: 0;
    letter-spacing: 2px;
    color: var(--accent-purple);
    font-weight: 600;
}

.navbar {
    display: flex;
    gap: 2rem;
    align-items: center;
}

.nav-link {
    color: var(--white-primary);
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s ease;
    position: relative;
}

.nav-link:hover {
    color: var(--accent-purple);
}

.nav-link::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 0;
    width: 0;
    height: 2px;
    background: var(--accent-purple);
    transition: width 0.3s ease;
}

.nav-link:hover::after {
    width: 100%;
}

.menu-toggle {
    display: none;
    flex-direction: column;
    background: none;
    border: none;
    cursor: pointer;
    gap: 5px;
}

.menu-toggle span {
    width: 25px;
    height: 3px;
    background: var(--white-primary);
    border-radius: 2px;
    transition: all 0.3s ease;
}

.footer {
    background: var(--navy-primary);
    color: var(--white-primary);
    padding: 3rem 2rem 1rem;
    margin-top: 4rem;
}

.footer-content {
    max-width: 1400px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.footer-section h3,
.footer-section h4 {
    margin-bottom: 1rem;
    color: var(--accent-purple);
}

.footer-section p {
    margin-bottom: 0.5rem;
    opacity: 0.9;
    font-size: 0.95rem;
}

.footer-section ul {
    list-style: none;
}

.footer-section ul li {
    margin-bottom: 0.5rem;
}

.footer-section ul li a {
    color: var(--white-primary);
    text-decoration: none;
    transition: all 0.3s ease;
}

.footer-section ul li a:hover {
    color: var(--accent-purple);
    padding-left: 5px;
}

.footer-bottom {
    text-align: center;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    opacity: 0.8;
    font-size: 0.9rem;
}

.main-content {
    min-height: calc(100vh - 200px);
    max-width: 1400px;
    margin: 0 auto;
    width: 100%;
}

.hero-section {
    background: radial-gradient(circle at top left, rgba(15, 38, 81, 0.18), transparent 34%),
                linear-gradient(180deg, #ffffff 0%, #eef4ff 45%, #ffffff 100%);
    color: var(--navy-primary);
    padding: 4rem 2rem;
    margin-bottom: 3rem;
    position: relative;
}

.hero-badge {
    display: inline-block;
    background: var(--navy-primary);
    color: var(--white-primary);
    padding: 0.65rem 1rem;
    border-radius: 999px;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
    letter-spacing: 1px;
}

.hero-content {
    background: var(--white-primary);
    padding: 3rem;
    border-radius: 24px;
    box-shadow: 0 24px 70px rgba(22, 37, 67, 0.08);
    border-left: 10px solid #0f2651;
    display: flex;
    flex-direction: column;
    justify-content: center;
    color: var(--navy-primary);
}

.hero-content h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
    font-weight: 700;
    line-height: 1.05;
}

.hero-subtitle {
    font-size: 1.6rem;
    margin-bottom: 1rem;
    opacity: 0.95;
}

.hero-description {
    font-size: 1.12rem;
    margin-bottom: 2rem;
    opacity: 0.9;
    max-width: 750px;
}

.hero-actions {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin-bottom: 2rem;
}

.cta-button {
    display: inline-block;
    padding: 0.85rem 2.5rem;
    background: var(--accent-purple);
    color: var(--white-primary);
    text-decoration: none;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.3s ease;
    border: 2px solid var(--accent-purple);
    cursor: pointer;
    font-size: 1rem;
}

.cta-button:hover {
    background: transparent;
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(124, 58, 237, 0.3);
}

.cta-button.secondary {
    background: transparent;
    border: 2px solid rgba(255, 255, 255, 0.85);
    color: var(--navy-primary);
}

.cta-button-large {
    display: inline-block;
    padding: 1rem 3rem;
    background: var(--accent-purple);
    color: var(--white-primary);
    text-decoration: none;
    border-radius: 8px;
    font-weight: 700;
    transition: all 0.3s ease;
    font-size: 1.1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.cta-button-large:hover {
    background: var(--accent-blue);
    transform: translateY(-3px);
    box-shadow: 0 15px 30px rgba(59, 130, 246, 0.3);
}

.hero-highlights {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
}

.hero-highlights div {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 18px;
    padding: 1.25rem;
}

.hero-highlights h4 {
    margin-bottom: 0.5rem;
    color: var(--navy-primary);
}

.hero-highlights p {
    color: var(--text-light);
    font-size: 0.95rem;
    margin: 0;
}

.company-overview {
    padding: 3rem 2rem;
    background: var(--white-secondary);
}

.company-overview h2,
.reviews-section h2,
.services-details h2,
.tech-stack h2,
.service-packages h2,
.faq-section h2,
.quick-contact h2 {
    text-align: center;
    font-size: 2.5rem;
    color: var(--navy-primary);
    margin-bottom: 0.5rem;
}

.overview-grid,
.tech-grid,
.packages-container,
.faq-container,
.quick-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
    max-width: 1400px;
    margin-left: auto;
    margin-right: auto;
}

.overview-card,
.detail-card,
.quick-card {
    background: var(--white-primary);
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
    transition: all 0.3s ease;
    border: 2px solid transparent;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.overview-card:hover,
.detail-card:hover,
.quick-card:hover {
    transform: translateY(-5px);
    border-color: var(--accent-purple);
    box-shadow: 0 10px 30px rgba(124, 58, 237, 0.2);
}

.card-icon,
.detail-icon,
.quick-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.overview-card h3,
.detail-card h4,
.quick-card h4 {
    color: var(--navy-primary);
    margin-bottom: 0.5rem;
}

.overview-card p,
.detail-card p,
.quick-card p {
    color: var(--text-light);
    font-size: 0.95rem;
}

.reviews-section {
    padding: 3rem 2rem;
    background: var(--white-primary);
}

.reviews-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin: 2rem auto;
    max-width: 1400px;
}

.review-card {
    background: var(--white-secondary);
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 4px solid var(--accent-purple);
    transition: all 0.3s ease;
}

.review-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.review-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
}

.reviewer-info {
    display: flex;
    gap: 1rem;
}

.avatar {
    width: 45px;
    height: 45px;
    background: linear-gradient(135deg, var(--accent-purple), var(--accent-blue));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
}

.reviewer-info h4 {
    color: var(--navy-primary);
    margin: 0;
    font-size: 1rem;
}

.company {
    color: var(--text-light);
    font-size: 0.85rem;
    margin: 0.25rem 0 0;
}

.rating {
    text-align: right;
}

.stars {
    display: block;
    font-size: 1rem;
}

.rating-value {
    color: var(--accent-purple);
    font-weight: 700;
    font-size: 0.9rem;
}

.review-text {
    color: var(--text-dark);
    font-style: italic;
    line-height: 1.6;
}

.average-rating {
    grid-column: 1 / -1;
    background: linear-gradient(135deg, var(--navy-primary), var(--navy-light));
    color: var(--white-primary);
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
    margin-top: 2rem;
}

.average-rating h3 {
    margin-bottom: 1rem;
}

.rating-display {
    margin-bottom: 1rem;
}

.big-rating {
    font-size: 3rem;
    font-weight: 700;
}

.out-of {
    font-size: 1.5rem;
    opacity: 0.9;
}

.stats-section {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    padding: 3rem 2rem;
    background: linear-gradient(135deg, var(--navy-primary), var(--navy-light));
    margin: 3rem auto;
    max-width: 1400px;
}

.stat-card {
    background: rgba(255, 255, 255, 0.1);
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
    color: var(--white-primary);
    border: 2px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;
}

.stat-card:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: translateY(-5px);
}

.stat-card h3 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.stat-card p {
    font-size: 1.1rem;
    opacity: 0.9;
}

.services-showcase {
    padding: 3rem 2rem;
    background: var(--white-primary);
}

.showcase-header {
    text-align: center;
    margin-bottom: 2rem;
}

.showcase-header h2 {
    font-size: 2.5rem;
    color: var(--navy-primary);
}

.showcase-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1.5rem;
    max-width: 1400px;
    margin: 0 auto 2rem;
}

.showcase-service {
    background: var(--white-secondary);
    padding: 1.5rem;
    border-radius: 10px;
    text-align: center;
    transition: all 0.3s ease;
    border: 2px solid transparent;
}

.showcase-service:hover {
    border-color: var(--accent-purple);
    transform: translateY(-3px);
}

.showcase-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

.showcase-service h4 {
    color: var(--navy-primary);
    font-size: 0.95rem;
    margin-bottom: 0.5rem;
}

.showcase-service p {
    color: var(--text-light);
    font-size: 0.85rem;
}

.showcase-cta {
    text-align: center;
}

.services-hero,
.contact-hero {
    background: linear-gradient(135deg, var(--navy-primary) 0%, var(--navy-light) 100%);
    color: var(--white-primary);
    padding: 3rem 2rem;
    text-align: center;
}

.services-hero h1,
.contact-hero h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.services-main {
    padding: 3rem 2rem;
    background: var(--white-secondary);
}

.services-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    max-width: 1400px;
    margin: 0 auto;
}

.service-card {
    background: var(--white-primary);
    border-radius: 10px;
    overflow: hidden;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    position: relative;
    min-height: 250px;
    cursor: pointer;
}

.service-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 35px rgba(124, 58, 237, 0.25);
}

.service-card.active-service {
    box-shadow: 0 15px 40px rgba(124, 58, 237, 0.35);
    border: 2px solid var(--accent-purple);
}

.service-card.active-service .service-main {
    opacity: 0.2;
    pointer-events: none;
}

.service-main {
    padding: 2rem;
    text-align: center;
}

.service-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.service-main h3 {
    color: var(--navy-primary);
    margin-bottom: 0.5rem;
    font-size: 1.3rem;
}

.service-description {
    color: var(--text-light);
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

.hover-hint {
    color: var(--accent-purple);
    font-size: 0.85rem;
    font-weight: 600;
}

.subcategories-dropdown {
    display: none;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, var(--navy-primary), var(--navy-light));
    color: var(--white-primary);
    padding: 1.5rem;
    border-radius: 10px;
    overflow-y: auto;
    animation: slideIn 0.3s ease;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.subcategories-header {
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.subcategories-header h4 {
    font-size: 1.1rem;
    margin: 0;
}

.subcategories-list {
    list-style: none;
    margin-bottom: 1rem;
}

.subcategory-item {
    padding: 0.6rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    opacity: 0.9;
    transition: all 0.2s ease;
}

.subcategory-item:hover {
    opacity: 1;
    transform: translateX(5px);
}

.checkbox {
    color: var(--accent-purple);
    font-weight: bold;
}

.inquiry-btn {
    padding: 0.6rem 1.5rem;
    background: var(--accent-purple);
    color: var(--white-primary);
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
}

.inquiry-btn:hover {
    background: var(--accent-blue);
    transform: translateY(-2px);
}

.services-details {
    padding: 3rem 2rem;
    background: var(--white-primary);
}

.details-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
    max-width: 1400px;
    margin-left: auto;
    margin-right: auto;
}

.tech-stack {
    padding: 3rem 2rem;
    background: var(--white-secondary);
}

.tech-category {
    background: var(--white-primary);
    padding: 1.5rem;
    border-radius: 8px;
    border-left: 4px solid var(--accent-purple);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.tech-category h4 {
    color: var(--navy-primary);
    margin-bottom: 0.5rem;
}

.tech-category p {
    color: var(--text-light);
    font-size: 0.9rem;
}

.service-packages {
    padding: 3rem 2rem;
    background: var(--white-primary);
}

.package {
    background: var(--white-secondary);
    padding: 2rem;
    border-radius: 10px;
    border: 2px solid var(--border-color);
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
}

.package:hover {
    transform: translateY(-5px);
    border-color: var(--accent-purple);
    box-shadow: 0 10px 30px rgba(124, 58, 237, 0.1);
}

.package.featured {
    transform: scale(1.05);
    background: linear-gradient(135deg, var(--navy-primary), var(--navy-light));
    color: var(--white-primary);
    border-color: var(--accent-purple);
}

.package.featured:hover {
    transform: scale(1.05) translateY(-5px);
}

.badge {
    position: absolute;
    top: 10px;
    right: 10px;
    background: var(--accent-purple);
    color: var(--white-primary);
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 700;
}

.package h3 {
    color: var(--navy-primary);
    margin-bottom: 0.5rem;
    font-size: 1.5rem;
}

.package.featured h3 {
    color: var(--white-primary);
}

.price {
    font-size: 1.3rem;
    color: var(--accent-purple);
    margin-bottom: 1.5rem;
    font-weight: 700;
}

.features-list {
    list-style: none;
    text-align: left;
    margin-bottom: 1.5rem;
}

.features-list li {
    padding: 0.6rem 0;
    color: var(--text-dark);
}

.package.featured .features-list li {
    color: var(--white-primary);
}

.package-btn {
    width: 100%;
    padding: 0.75rem;
    background: var(--accent-blue);
    color: var(--white-primary);
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
}

.package-btn:hover {
    background: var(--accent-purple);
    transform: translateY(-2px);
}

.contact-section {
    max-width: 1400px;
    margin: 3rem auto;
    padding: 0 2rem;
}

.contact-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
}

.contact-info h2,
.contact-form-wrapper h2 {
    color: var(--navy-primary);
    margin-bottom: 1.5rem;
    font-size: 1.8rem;
}

.info-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.info-card {
    background: var(--white-secondary);
    padding: 1.5rem;
    border-radius: 8px;
    text-align: center;
    border-left: 4px solid var(--accent-purple);
    transition: all 0.3s ease;
}

.info-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.info-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

.info-card h4 {
    color: var(--navy-primary);
    margin-bottom: 0.5rem;
}

.info-card p {
    color: var(--text-light);
    font-size: 0.9rem;
}

.subtext {
    font-size: 0.8rem;
    opacity: 0.8;
}

.company-details {
    background: linear-gradient(135deg, var(--navy-primary), var(--navy-light));
    color: var(--white-primary);
    padding: 1.5rem;
    border-radius: 8px;
    margin-top: 1rem;
}

.company-details h3 {
    margin-bottom: 1rem;
    color: var(--accent-purple);
}

.company-details p {
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
}

.contact-form {
    background: var(--white-secondary);
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    color: var(--navy-primary);
    font-weight: 600;
}

.form-group input,
.form-group textarea,
.form-group select {
    width: 100%;
    padding: 0.75rem;
    border: 2px solid var(--border-color);
    border-radius: 6px;
    font-size: 0.95rem;
    font-family: inherit;
    transition: all 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus,
.form-group select:focus {
    outline: none;
    border-color: var(--accent-blue);
    box-shadow: 0 0 8px rgba(59, 130, 246, 0.2);
}

.form-group textarea {
    resize: vertical;
}

.form-group.checkbox {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.form-group.checkbox input {
    width: auto;
    margin: 0;
}

.checkbox-label {
    margin: 0;
    color: var(--text-dark);
    font-weight: 400;
}

.submit-btn {
    width: 100%;
    padding: 0.85rem;
    background: linear-gradient(135deg, var(--navy-primary), var(--accent-blue));
    color: var(--white-primary);
    border: none;
    border-radius: 6px;
    font-weight: 700;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.submit-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(0, 26, 77, 0.3);
}

.form-message {
    margin-top: 1rem;
    padding: 1rem;
    border-radius: 6px;
    text-align: center;
    display: none;
}

.form-message.success {
    display: block;
    background-color: #d4edda;
    color: var(--success-color);
    border: 1px solid var(--success-color);
}

.form-message.error {
    display: block;
    background-color: #f8d7da;
    color: var(--error-color);
    border: 1px solid var(--error-color);
}

.faq-section {
    padding: 3rem 2rem;
    background: var(--white-secondary);
}

.faq-item {
    background: var(--white-primary);
    padding: 1.5rem;
    border-radius: 8px;
    border-left: 4px solid var(--accent-purple);
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}

.faq-item:hover {
    transform: translateX(5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
}

.faq-item h4 {
    color: var(--navy-primary);
    margin-bottom: 0.5rem;
    cursor: pointer;
}

.faq-item p {
    color: var(--text-light);
    font-size: 0.95rem;
    line-height: 1.6;
}

.quick-contact {
    padding: 3rem 2rem;
    background: var(--white-primary);
}

.quick-cards {
    margin-top: 2rem;
    max-width: 1400px;
    margin-left: auto;
    margin-right: auto;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}

.quick-card {
    text-decoration: none;
    color: inherit;
    background: var(--white-secondary);
    border: 2px solid var(--border-color);
    padding: 2rem;
    border-radius: 10px;
    text-align: center;
    transition: all 0.3s ease;
}

.quick-card:hover {
    border-color: var(--accent-purple);
    transform: translateY(-5px);
}

.quick-action {
    color: var(--accent-purple);
    font-weight: 600;
    font-size: 0.9rem;
    display: block;
    margin-top: 0.5rem;
}

.cta-section {
    background: linear-gradient(135deg, var(--navy-primary), var(--navy-light));
    color: var(--white-primary);
    padding: 3rem 2rem;
    text-align: center;
    margin-top: 3rem;
}

.cta-section h2 {
    font-size: 2.2rem;
    margin-bottom: 1rem;
}

.cta-section p {
    font-size: 1.1rem;
    margin-bottom: 2rem;
    opacity: 0.95;
}

.about-hero {
    padding: 4rem 2rem;
    background: linear-gradient(135deg, rgba(15, 38, 81, 0.18), rgba(255, 255, 255, 0.98));
    margin-bottom: 2rem;
    border-radius: 32px;
}

.about-hero-content {
    max-width: 900px;
    margin: 0 auto;
}

.about-section {
    padding: 3rem 2rem;
    max-width: 1400px;
    margin: 0 auto 2rem;
}

.section-header {
    text-align: center;
    margin-bottom: 2rem;
}

.section-header h2 {
    font-size: 2.5rem;
    color: var(--navy-primary);
}

.about-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.5rem;
}

.about-card {
    background: var(--white-primary);
    border-radius: 24px;
    padding: 2rem;
    box-shadow: 0 20px 40px rgba(15, 38, 81, 0.06);
    border: 1px solid rgba(15, 38, 81, 0.06);
}

.about-card h3 {
    margin-bottom: 1rem;
    color: var(--navy-primary);
}

.about-card p {
    color: #4f617f;
}

.strength-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8faff 100%);
    border-radius: 24px;
    padding: 2.5rem;
    box-shadow: 0 20px 40px rgba(15, 38, 81, 0.08);
    border: 1px solid rgba(15, 38, 81, 0.08);
    transition: all 0.3s ease;
}

.strength-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 30px 60px rgba(15, 38, 81, 0.12);
}

.strength-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.strength-card h3 {
    margin-bottom: 1rem;
    color: var(--navy-primary);
    font-size: 1.2rem;
}

.strength-card p {
    color: #4f617f;
    line-height: 1.6;
}

.promise-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
}

.promise-card {
    background: var(--white-primary);
    border-radius: 24px;
    padding: 2rem;
    box-shadow: 0 20px 40px rgba(15, 38, 81, 0.06);
    border: 2px solid rgba(124, 58, 237, 0.1);
    transition: all 0.3s ease;
}

.promise-card:hover {
    border-color: rgba(124, 58, 237, 0.3);
    box-shadow: 0 25px 50px rgba(124, 58, 237, 0.1);
}

.promise-card h3 {
    color: var(--navy-primary);
    margin-bottom: 1rem;
    font-size: 1.1rem;
}

.promise-card p {
    color: #4f617f;
    line-height: 1.6;
}

.about-cta {
    text-align: center;
    padding: 3rem 2rem;
    background: linear-gradient(135deg, #0f2651 0%, #1a3a7a 100%);
    border-radius: 32px;
    color: var(--white-primary);
    margin: 3rem auto;
    max-width: 900px;
}

.about-cta h2 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: var(--white-primary);
}

.about-cta p {
    font-size: 1.1rem;
    margin-bottom: 2rem;
    color: rgba(255, 255, 255, 0.9);
}

.cta-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

.chatbot-toggle {
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent-purple), var(--accent-blue));
    border: none;
    font-size: 1.8rem;
    cursor: pointer;
    box-shadow: 0 5px 20px rgba(124, 58, 237, 0.4);
    transition: all 0.3s ease;
    z-index: 999;
    display: flex;
    align-items: center;
    justify-content: center;
}

.chatbot-toggle:hover {
    transform: scale(1.1);
    box-shadow: 0 8px 25px rgba(124, 58, 237, 0.6);
}

.chatbot-widget {
    position: fixed;
    bottom: 100px;
    right: 30px;
    width: 350px;
    background: var(--white-primary);
    border-radius: 12px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    display: none;
    flex-direction: column;
    z-index: 998;
    animation: slideUp 0.4s ease;
}

.chatbot-widget.active {
    display: flex;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.chatbot-header {
    background: linear-gradient(135deg, var(--navy-primary), var(--navy-light));
    color: var(--white-primary);
    padding: 1rem;
    border-radius: 12px 12px 0 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.chatbot-header h3 {
    margin: 0;
    font-size: 1.1rem;
}

.chatbot-close {
    background: none;
    border: none;
    color: var(--white-primary);
    font-size: 1.5rem;
    cursor: pointer;
    transition: all 0.2s ease;
}

.chatbot-close:hover {
    transform: rotate(90deg);
}

.chatbot-messages {
    height: 300px;
    overflow-y: auto;
    padding: 1rem;
    background: #f8f9fa;
    flex: 1;
}

.chatbot-message {
    margin-bottom: 0.8rem;
    animation: slideIn 0.3s ease;
}

.chatbot-message p {
    margin: 0;
    padding: 0.8rem 1rem;
    border-radius: 8px;
    max-width: 90%;
    word-wrap: break-word;
    line-height: 1.4;
}

.user-message p {
    background: var(--accent-purple);
    color: white;
    margin-left: auto;
    border-radius: 15px 15px 0 15px;
}

.bot-message p {
    background: #e5e7eb;
    color: var(--text-dark);
    border-radius: 15px 15px 15px 0;
}

.bot-message.loading p {
    background: #fff3cd;
    color: #856404;
}
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}

.chatbot-message {
    padding: 0.8rem 1rem;
    border-radius: 8px;
    max-width: 90%;
    word-wrap: break-word;
    font-size: 0.9rem;
    line-height: 1.4;
}

.bot-message {
    background: var(--white-secondary);
    color: var(--navy-primary);
    border-left: 3px solid var(--accent-purple);
    align-self: flex-start;
}

.user-message {
    background: linear-gradient(135deg, var(--accent-purple), var(--accent-blue));
    color: var(--white-primary);
    align-self: flex-end;
}

.chatbot-input-area {
    display: flex;
    gap: 0.5rem;
    padding: 1rem;
    border-top: 1px solid var(--border-color);
    background: var(--white-secondary);
    border-radius: 0 0 12px 12px;
}

.chatbot-input {
    flex: 1;
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 0.6rem;
    font-size: 0.9rem;
    transition: all 0.2s ease;
}

.chatbot-input:focus {
    outline: none;
    border-color: var(--accent-purple);
    box-shadow: 0 0 8px rgba(124, 58, 237, 0.2);
}

.chatbot-send {
    padding: 0.6rem 1rem;
    background: var(--accent-purple);
    color: var(--white-primary);
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s ease;
}

.chatbot-send:hover {
    background: var(--accent-blue);
}

@media (max-width: 1024px) {
    .contact-container {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 768px) {
    .menu-toggle {
        display: flex;
    }

    .navbar {
        display: none;
    }

    .hero-content h1 {
        font-size: 2rem;
    }

    .company-overview h2,
    .reviews-section h2,
    .services-details h2,
    .tech-stack h2,
    .service-packages h2,
    .faq-section h2,
    .quick-contact h2,
    .services-hero h1,
    .contact-hero h1 {
        font-size: 1.8rem;
    }

    .services-container {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 480px) {
    .company-info h1 {
        font-size: 1.1rem;
    }

    .hero-content {
        padding: 1.5rem;
    }

    .hero-content h1 {
        font-size: 1.5rem;
    }

    .cta-button {
        padding: 0.7rem 1.5rem;
        font-size: 0.9rem;
    }

    .overview-grid,
    .reviews-container,
    .stats-section,
    .showcase-grid,
    .details-grid,
    .tech-grid,
    .packages-container,
    .faq-container,
    .quick-cards,
    .services-container {
        grid-template-columns: 1fr;
    }

    .package.featured {
        transform: scale(1);
    }

    .chatbot-widget {
        width: 90%;
        bottom: 80px;
        right: 5%;
        left: 5%;
    }
}

/* =====================
   MISSING ANIMATIONS
   ===================== */

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideInFromLeft {
    from {
        opacity: 0;
        transform: translateX(-100px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideInFromRight {
    from {
        opacity: 0;
        transform: translateX(100px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-in {
    animation: slideDown 0.8s ease forwards;
}

.hero-title-container {
    overflow: hidden;
    display: block;
}

#welcome-text, #micromatrix-text {
    display: inline-block;
    opacity: 1;
}

#welcome-text {
    color: var(--accent-purple);
    font-weight: 700;
    transform: translateX(-120%);
}

#micromatrix-text {
    color: var(--accent-blue);
    font-weight: 700;
    transform: translateX(120%);
}
"""

# =====================
# JAVASCRIPT CONTENT
# =====================

JS_CONTENT = """
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

    // Welcome slides in from left (-120% to 0)
    animateSlideIn(welcomeText, -120, 800, 200);

    // Micromatrix slides in from right (120% to 0) with a delay
    animateSlideIn(micromatrixText, 120, 800, 400);
});

// =====================
// NAVIGATION TOGGLE
// =====================

function toggleMenu() {
    const navbar = document.getElementById('navbar');
    const menuToggle = document.getElementById('menuToggle');
    
    navbar.classList.toggle('active');
    menuToggle.classList.toggle('active');
}

document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        const navbar = document.getElementById('navbar');
        const menuToggle = document.getElementById('menuToggle');
        navbar.classList.remove('active');
        menuToggle.classList.remove('active');
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
document.querySelectorAll('a[href^=\"#\"]').forEach(anchor => {
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
"""

# =====================
# FLASK ROUTES
# =====================

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    content = render_template_string(HOME_TEMPLATE, reviews=reviews)
    html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content)
    html = render_template_string(html, css_content=CSS_CONTENT, js_content=JS_CONTENT)
    return html

@app.route('/services')
def services():
    content = render_template_string(SERVICES_TEMPLATE, services=services_data, pricing=pricing_data)
    html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content)
    html = render_template_string(html, css_content=CSS_CONTENT, js_content=JS_CONTENT)
    return html

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        
        contact_data = {
            'name': name,
            'email': email,
            'phone': phone,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            owner_email_body = f"""
New Contact/Order Inquiry from Micromatrix Website

Client Details:
Name: {name}
Email: {email}
Phone: {phone}
Date & Time: {contact_data['timestamp']}

Message/Project Details:
{message}

This is an automated notification from your Micromatrix website.
Please respond to the client at their email or phone number above.
            """
            
            owner_msg = Message(
                subject=f'New Order/Inquiry: {name} - Micromatrix',
                recipients=[OWNER_EMAIL],
                body=owner_email_body
            )
            
            user_email_body = f"""
Hello {name},

Thank you for contacting Micromatrix! We have received your inquiry and will get back to you shortly.

Your Details:
Name: {name}
Email: {email}
Phone: {phone}
Received on: {contact_data['timestamp']}

Your Message:
{message}

Our team will review your request and contact you within 24 hours.

Best regards,
Muhammad Asif
Founder, Micromatrix
info@micromatrix.tech
+923316170980
            """
            
            user_msg = Message(
                subject='We Received Your Inquiry - Micromatrix',
                recipients=[email],
                body=user_email_body
            )
            
            try:
                mail.send(owner_msg)
                mail.send(user_msg)
            except:
                pass
            
            return jsonify({
                'status': 'success',
                'message': 'Thank you for your inquiry! We will contact you within 24 hours.',
                'data': contact_data
            })
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({
                'status': 'success',
                'message': 'Thank you for your inquiry! We will contact you within 24 hours.',
                'data': contact_data
            }), 200
    
    html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', render_template_string(CONTACT_TEMPLATE, pricing=pricing_data))
    html = render_template_string(html, css_content=CSS_CONTENT, js_content=JS_CONTENT)
    return html

@app.route('/about')
def about():
    html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', render_template_string(ABOUT_TEMPLATE))
    html = render_template_string(html, css_content=CSS_CONTENT, js_content=JS_CONTENT)
    return html

@app.route('/api/services')
def api_services():
    return jsonify(services_data)

@app.route('/api/reviews')
def api_reviews():
    return jsonify(reviews)

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get('message', '').lower().strip()
    if not user_message:
        return jsonify({'response': 'Please ask me a question about Micromatrix.'})
    if user_message in chatbot_knowledge:
        return jsonify({'response': chatbot_knowledge[user_message]})
    for key, value in chatbot_knowledge.items():
        if key in user_message or user_message in key:
            return jsonify({'response': value})
    default_response = (
        "That's a great question! I'm still learning. However, you can always reach our team at "
        "+923316170980 or info@micromatrix.tech for more detailed information. "
        "You can also visit our Services page to explore what we offer, or use the Contact page to send us a message."
    )
    return jsonify({'response': default_response})

if __name__ == '__main__':
    print("=" * 50)
    print("MICROMATRIX - COMPLETE APPLICATION")
    print("=" * 50)
    print("\nStarting Flask application...")
    print("Navigate to: http://localhost:5000")
    print("\nPages available:")
    print("  - Home: http://localhost:5000/home")
    print("  - Services: http://localhost:5000/services")
    print("  - Contact: http://localhost:5000/contact")
    print("  - About: http://localhost:5000/about")
    print("\nPress CTRL+C to stop the server\n")
    app.run(debug=True, port=5000, host='0.0.0.0')
