"""
MICROMATRIX - COMPLETE APPLICATION IN ONE FILE
All backend, frontend, HTML, CSS, and JavaScript combined into a single Python file
Flask Application with Embedded Templates and Assets
"""

from flask import Flask, render_template_string, request, jsonify, redirect, url_for, session, flash
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import os
import sqlite3

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
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'asifhavelilakha@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '') # SET THIS IN ENV VAR
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'asifhavelilakha@gmail.com')

mail = Mail(app)

OWNER_EMAIL = 'asifhavelilakha@gmail.com'
OWNER_NAME = 'Asif - Micromatrix Admin'

# =====================
# DATABASE SETUP
# =====================
# Use /tmp for database on Vercel since the filesystem is read-only
if os.environ.get('VERCEL'):
    DB_NAME = '/tmp/micromatrix.db'
else:
    DB_NAME = 'micromatrix.db'

def init_db():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT,
                    service TEXT,
                    budget TEXT,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Create default admin if not exists
            admin_email = 'asifhavelilakha@gmail.com'
            admin_pass = 'asif1632'
            cursor.execute('SELECT id FROM users WHERE email = ?', (admin_email,))
            if not cursor.fetchone():
                cursor.execute(
                    'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                    ('Asif Admin', admin_email, generate_password_hash(admin_pass))
                )
            conn.commit()
    except Exception as e:
        print(f"Database initialization failed: {str(e)}")

# Initialize DB on startup
try:
    init_db()
except:
    pass

# =====================
# DATA STRUCTURES
# =====================

reviews = [
    {'name': 'Ahmed Hassan', 'company': 'Tech Solutions Inc', 'rating': 5, 'text': 'Micromatrix delivered an outstanding ERP system for our company. Professional team and excellent support!', 'image': '<i class="fas fa-user-circle"></i>'},
    {'name': 'Fatima Khan', 'company': 'E-Commerce Hub', 'rating': 5, 'text': 'The e-commerce website they developed increased our sales by 150%. Highly recommended!', 'image': '<i class="fas fa-user-circle"></i>'},
    {'name': 'Muhammad Ali', 'company': 'Digital Marketing Pro', 'rating': 4.8, 'text': 'Great mobile app development team. They delivered on time and within budget.', 'image': '<i class="fas fa-user-circle"></i>'},
    {'name': 'Sarah Johnson', 'company': 'Finance Corp', 'rating': 5, 'text': 'Their fintech solutions are cutting edge. Very professional and innovative team.', 'image': '<i class="fas fa-user-circle"></i>'},
    {'name': 'Rizwan Sheikh', 'company': 'AI StartUp', 'rating': 4.9, 'text': 'The AI and machine learning solutions transformed our business processes.', 'image': '<i class="fas fa-user-circle"></i>'},
    {'name': 'David Chen', 'company': 'Global Logistics', 'rating': 5, 'text': 'We partnered with Micromatrix for cloud migration. The transition was flawless, saving us significant operational costs.', 'image': '<i class="fas fa-user-circle"></i>'},
    {'name': 'Aisha Patel', 'company': 'HealthTech Solutions', 'rating': 4.9, 'text': 'Their UI/UX team redesigned our patient portal. User engagement skyrocketed within the first month. Excellent work!', 'image': '<i class="fas fa-user-circle"></i>'},
    {'name': 'James Miller', 'company': 'Retail Enterprises', 'rating': 4.8, 'text': 'Micromatrix provided excellent IT consulting. They understood our requirements perfectly and suggested the best tech stack.', 'image': '<i class="fas fa-user-circle"></i>'},
    {'name': 'Elena Rodriguez', 'company': 'EduPlatform', 'rating': 5, 'text': 'The dedicated remote team felt like an extension of our own staff. Communication was transparent and deliverables were on point.', 'image': '<i class="fas fa-user-circle"></i>'},
    {'name': 'Tariq Mahmood', 'company': 'AutoParts Direct', 'rating': 5, 'text': 'Implementing their custom CRM solution streamlined our workflow drastically. I highly recommend Micromatrix for custom software.', 'image': '<i class="fas fa-user-circle"></i>'}
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
    'owner': 'Micromatrix is led by Muhammad Asif from Pakistan.',
    'founder': 'Micromatrix was founded by Muhammad Asif in 2020.',
    'pricing': 'Our pricing is structured into Starter ($100-$500), Basic ($500-$1000), and Professional ($1000-$2000) tiers. It varies based on your project requirements.',
    'process': 'We start with a detailed assessment, followed by an estimated timeline. We maintain transparent communication and ensure rigorous testing throughout the process.',
    'hello': 'Hello! Welcome to Micromatrix. How can I help you today?',
    'hi': "Hi there! I'm the Micromatrix Assistant. Feel free to ask me anything about our services or company.",
    'help': 'I can help you with information about Micromatrix services, pricing, contact details, or any questions about our company. What would you like to know?',
    'thanks': "You're welcome! Feel free to ask me anything else about Micromatrix.",
    'thank you': "My pleasure! Is there anything else you'd like to know?"
}

services_data = {
    'Software Development': {'icon': '<i class="fas fa-laptop-code"></i>', 'description': 'Complete software solutions tailored to your business needs', 'subcategories': ['Custom Software Development', 'Enterprise Software (ERP systems)', 'CRM (Customer Relationship Management Systems)', 'Desktop Applications']},
    'Web Development': {'icon': '<i class="fas fa-globe"></i>', 'description': 'Modern web solutions for your online presence', 'subcategories': ['Website Design (UI/UX)', 'Frontend + Backend Development', 'E-commerce websites (Shopify, WooCommerce)', 'CMS (WordPress, Joomla)']},
    'Mobile App Development': {'icon': '<i class="fas fa-mobile-alt"></i>', 'description': 'High-performance mobile applications', 'subcategories': ['Android App Development', 'iOS App Development', 'Cross-platform apps (Flutter, React Native)']},
    'Artificial Intelligence (AI) & Machine Learning': {'icon': '<i class="fas fa-robot"></i>', 'description': 'AI-powered solutions for modern businesses', 'subcategories': ['Chatbots', 'Automation systems', 'Data prediction models', 'Computer vision']},
    'Cloud Computing Services': {'icon': '<i class="fas fa-cloud"></i>', 'description': 'Scalable cloud infrastructure solutions', 'subcategories': ['Cloud hosting (AWS, Azure)', 'Cloud migration', 'SaaS solutions']},
    'Data Science & Analytics': {'icon': '<i class="fas fa-chart-bar"></i>', 'description': 'Transform data into actionable insights', 'subcategories': ['Data analysis', 'Business intelligence', 'Big data solutions']},
    'E-Commerce Solutions': {'icon': '<i class="fas fa-shopping-cart"></i>', 'description': 'Complete online store solutions', 'subcategories': ['Online store development', 'Payment gateway integration', 'Inventory systems']},
    'Digital Marketing Services': {'icon': '<i class="fas fa-bullhorn"></i>', 'description': 'Drive your online visibility and growth', 'subcategories': ['SEO (Search Engine Optimization)', 'Social Media Marketing', 'Google Ads / PPC', 'Content writing']},
    'Software Testing & QA': {'icon': '<i class="fas fa-check-circle"></i>', 'description': 'Ensure quality and reliability', 'subcategories': ['Manual testing', 'Automation testing', 'Performance testing']},
    'IT Consulting & Support': {'icon': '<i class="fas fa-wrench"></i>', 'description': 'Expert IT guidance and support', 'subcategories': ['Business IT consultancy', 'Technical support', 'System integration']},
    'Fintech & Banking Solutions': {'icon': '<i class="fas fa-credit-card"></i>', 'description': 'Secure financial technology solutions', 'subcategories': ['Digital banking apps', 'Payment systems', 'Leasing/finance software']},
    'ERP & Business Automation': {'icon': '<i class="fas fa-cogs"></i>', 'description': 'Automate and optimize business processes', 'subcategories': ['HR systems', 'Inventory systems', 'Accounting software']},
    'Game Development': {'icon': '<i class="fas fa-gamepad"></i>', 'description': 'Create engaging gaming experiences', 'subcategories': ['Mobile games', 'PC games', 'Unity / Unreal Engine projects']},
    'UI/UX Design Services': {'icon': '<i class="fas fa-paint-brush"></i>', 'description': 'Beautiful and intuitive user interfaces', 'subcategories': ['App design', 'Website interface design', 'User experience optimization']},
    'Emerging Technologies': {'icon': '<i class="fas fa-rocket"></i>', 'description': 'Future-ready technology solutions', 'subcategories': ['Blockchain development', 'IoT (Internet of Things)', 'AR/VR apps']}
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
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Outfit:wght@700;900&display=swap" rel="stylesheet">
    <link rel="preconnect" href="https://cdnjs.cloudflare.com" crossorigin>
    <link rel="dns-prefetch" href="https://cdnjs.cloudflare.com">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" media="print" onload="this.media='all'">
    <noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"></noscript>
    <style>
        {{ css_content|safe }}
    </style>
</head>
<body>
    <!-- Decorative Blobs -->
    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
    <div class="blob blob-3"></div>

    <header class="header">
        <div class="header-container">
            <!-- Logo on Left -->
            <div class="logo-header" onclick="window.location.href='/home'">
                <div class="logo-img-wrap">
                    <img src="/static/images/logo.png" alt="Micromatrix Logo" class="logo-img animated-logo">
                </div>
                <div class="company-info">
                    <h1>MICROMATRIX</h1>
                    <p>INNOVATIVE</p>
                </div>
            </div>

            <!-- Desktop Navigation + Hamburger on Right -->
            <div class="header-right">
                <nav class="navbar" id="navbar">
                    <a href="/home" class="nav-link">Home</a>
                    <a href="/about" class="nav-link">About</a>
                    <a href="/services" class="nav-link">Services</a>
                    <a href="/contact" class="nav-link">Contact Us</a>
                    {% if session.get('user_id') %}
                        {% if session.get('email') == 'asifhavelilakha@gmail.com' %}
                        <a href="/admin" class="nav-btn nav-btn-admin" style="background: var(--accent-yellow); color: var(--navy-dark);"><i class="fas fa-user-shield"></i> Admin Panel</a>
                        {% endif %}
                        <span class="nav-user"><i class="fas fa-user-circle"></i> {{ session.get('username', 'User') }}</span>
                        <a href="/logout" class="nav-btn nav-btn-logout"><i class="fas fa-sign-out-alt"></i> Logout</a>
                    {% else %}
                    <a href="/login" class="nav-btn nav-btn-login"><i class="fas fa-sign-in-alt"></i> Login</a>
                    <a href="/signup" class="nav-btn nav-btn-signup"><i class="fas fa-user-plus"></i> Sign Up</a>
                    {% endif %}
                </nav>

                <!-- Hamburger Toggle Button (Right Side) -->
                <button class="menu-toggle" id="menuToggle" onclick="toggleMenu()" aria-label="Toggle menu">
                    <span class="bar bar1"></span>
                    <span class="bar bar2"></span>
                    <span class="bar bar3"></span>
                </button>
            </div>
        </div>
    </header>

    <!-- Custom Cursor Follower -->
    <div class="cursor-glow" id="cursorGlow"></div>

    <!-- Live System Status -->
    <div class="system-status">
        <div class="status-dot"></div>
        <span id="statusPing">Systems Operational • Ping: 12ms</span>
    </div>

    <!-- Real-time Notifications -->

    <div id="notificationToast" class="notification-toast">
        <div class="notif-icon"><i class="fas fa-shopping-bag"></i></div>
        <div class="notif-content">
            <p id="notifMessage">New order from Dubai!</p>
            <span id="notifTime">2 minutes ago</span>
        </div>
    </div>

    <!-- Right Sidebar Overlay -->
    <div class="sidebar-overlay" id="sidebarOverlay" onclick="toggleMenu()"></div>

    <!-- Right Sidebar -->
    <aside class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <span>NAVIGATION</span>
            <button class="sidebar-close" onclick="toggleMenu()"><i class="fas fa-times"></i></button>
        </div>
        <nav class="sidebar-nav">
            <a href="/home" class="sidebar-link"><i class="fas fa-home"></i> Home</a>
            <a href="/about" class="sidebar-link"><i class="fas fa-info-circle"></i> About</a>
            <a href="/services" class="sidebar-link"><i class="fas fa-cogs"></i> Services</a>
            <a href="/contact" class="sidebar-link"><i class="fas fa-envelope"></i> Contact Us</a>
            {% if session.get('user_id') %}
            <a href="/logout" class="sidebar-link"><i class="fas fa-sign-out-alt"></i> Logout</a>
            {% else %}
            <a href="/login" class="sidebar-link"><i class="fas fa-sign-in-alt"></i> Login</a>
            <a href="/signup" class="sidebar-link"><i class="fas fa-user-plus"></i> Sign Up</a>
            {% endif %}
        </nav>
    </aside>

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
                <p><i class="fas fa-phone-alt"></i> Phone: +923316170980</p>
                <p><i class="fas fa-phone-alt"></i> Personal: +92 3039977330</p>
                <p><i class="fas fa-comment-dots"></i> WhatsApp: <a href="https://wa.me/923316170980" target="_blank" class="footer-link">+923316170980</a></p>
                <p><i class="fas fa-envelope"></i> Email: info@micromatrix.tech</p>
                <p><i class="fas fa-globe-americas"></i> Service: Global Remote Services</p>
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
        
        <!-- Live Visitor & Global Clocks -->
        <div class="footer-bottom">
            <p>&copy; 2026 Micromatrix. All rights reserved.</p>
            <div class="global-clocks" id="globalClocks">
                <div class="clock-item">
                    <span>New York</span>
                    <strong id="timeNY">--:--</strong>
                </div>
                <div class="clock-item">
                    <span>London</span>
                    <strong id="timeLDN">--:--</strong>
                </div>
                <div class="clock-item">
                    <span>Dubai</span>
                    <strong id="timeDXB">--:--</strong>
                </div>
                <div class="clock-item">
                    <span>Islamabad</span>
                    <strong id="timeISB">--:--</strong>
                </div>
            </div>
        </div>
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
                <p>Hi! <i class="fas fa-hand-paper"></i> I'm the Micromatrix Assistant. Ask me anything about our services, contact info, or company!</p>
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
        <i class="fas fa-comment-dots"></i>
    </button>

    <script>
        {{ js_content|safe }}
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
            <div class="founder-mini-card">
                <div class="founder-mini-avatar"><i class="fas fa-user-tie"></i></div>
                <div>
                    <strong>Muhammad Asif</strong> &mdash; Founder &amp; CEO
                    <span class="founder-mini-tag"><i class="fas fa-map-marker-alt"></i> Pakistan &nbsp;|&nbsp; <i class="fas fa-calendar-alt"></i> Est. 2020</span>
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
            <div class="card-icon"><i class="fas fa-globe-americas"></i></div>
            <h3>Global Remote Company</h3>
            <p>Operating worldwide with a distributed team of talented professionals</p>
        </div>
        <div class="overview-card">
            <div class="card-icon"><i class="fas fa-bolt"></i></div>
            <h3>Fast & Reliable</h3>
            <p>Quick turnaround times without compromising on quality</p>
        </div>
        <div class="overview-card">
            <div class="card-icon"><i class="fas fa-lock"></i></div>
            <h3>Secure Solutions</h3>
            <p>Enterprise-grade security for all our services and projects</p>
        </div>
        <div class="overview-card">
            <div class="card-icon"><i class="fas fa-rocket"></i></div>
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
                    <div class="avatar">{{ review.image|safe }}</div>
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
        <h2>Our Comprehensive Services</h2>
        <p>15 Specialized Technology Solutions for Your Business</p>
    </div>
    <div class="showcase-grid">
        <div class="showcase-service">
            <div class="showcase-icon"><i class="fas fa-laptop-code"></i></div>
            <h4>Software Development</h4>
            <p>Custom & Enterprise Solutions</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon"><i class="fas fa-globe"></i></div>
            <h4>Web Development</h4>
            <p>Modern Web Solutions</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon"><i class="fas fa-mobile-alt"></i></div>
            <h4>Mobile App Development</h4>
            <p>iOS, Android & Cross-Platform</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon"><i class="fas fa-robot"></i></div>
            <h4>AI & Machine Learning</h4>
            <p>Intelligent Automation</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon"><i class="fas fa-cloud"></i></div>
            <h4>Cloud Computing</h4>
            <p>AWS, Azure & SaaS</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon"><i class="fas fa-chart-bar"></i></div>
            <h4>Data Science</h4>
            <p>Analytics & Business Intelligence</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon"><i class="fas fa-shopping-cart"></i></div>
            <h4>E-Commerce Solutions</h4>
            <p>Complete Online Stores</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon"><i class="fas fa-bullhorn"></i></div>
            <h4>Digital Marketing</h4>
            <p>SEO, Social Media & Ads</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon"><i class="fas fa-check-circle"></i></div>
            <h4>Software Testing & QA</h4>
            <p>Quality Assurance</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon"><i class="fas fa-wrench"></i></div>
            <h4>IT Consulting</h4>
            <p>Expert Guidance & Support</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon"><i class="fas fa-credit-card"></i></div>
            <h4>Fintech Solutions</h4>
            <p>Banking & Payment Systems</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon"><i class="fas fa-cogs"></i></div>
            <h4>ERP & Automation</h4>
            <p>Business Process Automation</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon"><i class="fas fa-gamepad"></i></div>
            <h4>Game Development</h4>
            <p>Mobile & PC Games</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon"><i class="fas fa-paint-brush"></i></div>
            <h4>UI/UX Design</h4>
            <p>User Interface & Experience</p>
        </div>
        <div class="showcase-service">
            <div class="showcase-icon"><i class="fas fa-rocket"></i></div>
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
                <div class="service-icon">{{ service_data.icon|safe }}</div>
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
                        <span class="checkbox"><i class="fas fa-check"></i></span>
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
            <div class="detail-icon"><i class="fas fa-bullseye"></i></div>
            <h4>Focused Solutions</h4>
            <p>Each service is carefully crafted with specific business needs in mind</p>
        </div>
        <div class="detail-card">
            <div class="detail-icon"><i class="fas fa-bolt"></i></div>
            <h4>Fast Delivery</h4>
            <p>Quick implementation without compromising on quality standards</p>
        </div>
        <div class="detail-card">
            <div class="detail-icon"><i class="fas fa-lightbulb"></i></div>
            <h4>Innovation</h4>
            <p>Latest technologies and best practices to keep you ahead</p>
        </div>
        <div class="detail-card">
            <div class="detail-icon"><i class="fas fa-wrench"></i></div>
            <h4>Expert Team</h4>
            <p>Experienced professionals with proven track record</p>
        </div>
        <div class="detail-card">
            <div class="detail-icon"><i class="fas fa-chart-line"></i></div>
            <h4>Results Driven</h4>
            <p>Focused on delivering measurable business outcomes</p>
        </div>
        <div class="detail-card">
            <div class="detail-icon"><i class="fas fa-globe-americas"></i></div>
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
                    <div class="info-icon"><i class="fas fa-phone-alt"></i></div>
                    <h4>Phone Number</h4>
                    <p>+923316170980</p>
                    <p class="subtext">Available 24/7</p>
                </div>

                <div class="info-card">                    
                    <div class="info-icon"><i class="fas fa-mobile-alt"></i></div>
                    <h4>Secondary Number</h4>
                    <p><a href="tel:+923039977330" class="contact-link">+92 3039977330</a></p>
                    <p class="subtext">Direct support</p>
                </div>

                <div class="info-card">                    
                    <div class="info-icon"><i class="fas fa-comment-dots"></i></div>
                    <h4>WhatsApp</h4>
                    <p><a href="https://wa.me/923316170980" target="_blank" class="contact-link">+923316170980</a></p>
                    <p class="subtext">Quick chat support</p>
                </div>

                <div class="info-card">
                    <div class="info-icon"><i class="fas fa-envelope"></i></div>
                    <h4>Email Address</h4>
                    <p>info@micromatrix.tech</p>
                    <p class="subtext">Response within 24 hours</p>
                </div>

                <div class="info-card">
                    <div class="info-icon"><i class="fas fa-globe-americas"></i></div>
                    <h4>Global Reach</h4>
                    <p>Remote-First Company</p>
                    <p class="subtext">Serving clients worldwide</p>
                </div>

                <div class="info-card">
                    <div class="info-icon"><i class="fas fa-clock"></i></div>
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
            <div class="quick-icon"><i class="fas fa-phone-alt"></i></div>
            <h4>Call Us</h4>
            <p>+923316170980</p>
            <span class="quick-action">Click to call →</span>
        </a>

        <a href="mailto:info@micromatrix.tech" class="quick-card email-card">
            <div class="quick-icon"><i class="fas fa-envelope"></i></div>
            <h4>Email Us</h4>
            <p>info@micromatrix.tech</p>
            <span class="quick-action">Click to email →</span>
        </a>

        <div class="quick-card chat-card">
            <div class="quick-icon"><i class="fas fa-comment-dots"></i></div>
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

<!-- Founder / Owner Section -->
<section class="founder-section">
    <div class="section-header">
        <h2>Meet Our Founder</h2>
        <p>The vision and leadership behind Micromatrix</p>
    </div>
    <div class="founder-card">
        <div class="founder-avatar">
            <i class="fas fa-user-tie"></i>
        </div>
        <div class="founder-info">
            <h2>Muhammad Asif</h2>
            <p class="founder-title"><i class="fas fa-briefcase"></i> Founder &amp; CEO &mdash; Micromatrix</p>
            <p class="founder-location"><i class="fas fa-map-marker-alt"></i> Lahore, Pakistan &nbsp;&mdash;&nbsp; Remote Global Company</p>
            <p class="founder-since"><i class="fas fa-calendar-alt"></i> Founded in <strong>2020</strong> &mdash; Serving clients worldwide for 5+ years</p>
            <p class="founder-bio">Muhammad Asif is the founder and CEO of Micromatrix, a company he established in 2020 with a bold mission: to deliver world-class, affordable technology solutions from Pakistan to the global market. With deep expertise in software engineering, AI, cloud computing, and digital transformation, he assembled a talented remote-first team that serves businesses across multiple continents. Under his leadership, Micromatrix has grown to offer 15+ specialized services and has successfully delivered 100+ projects for startups and enterprises alike. His commitment to quality, transparency, and innovation defines the culture at Micromatrix.</p>
            <div class="founder-stats">
                <div class="f-stat">
                    <strong>5+</strong>
                    <span>Years Leading</span>
                </div>
                <div class="f-stat">
                    <strong>100+</strong>
                    <span>Projects Done</span>
                </div>
                <div class="f-stat">
                    <strong>15+</strong>
                    <span>Services</span>
                </div>
                <div class="f-stat">
                    <strong>Global</strong>
                    <span>Client Base</span>
                </div>
            </div>
            <div class="founder-contact">
                <a href="mailto:info@micromatrix.tech" class="founder-link"><i class="fas fa-envelope"></i> info@micromatrix.tech</a>
                <a href="https://wa.me/923316170980" class="founder-link" target="_blank"><i class="fab fa-whatsapp"></i> WhatsApp</a>
                <a href="tel:+923316170980" class="founder-link"><i class="fas fa-phone"></i> +92 331 617 0980</a>
            </div>
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
            <div class="strength-icon"><i class="fas fa-gem"></i></div>
            <h3>Exceptional Software Engineering</h3>
            <p>We develop software with uncompromising quality standards. Every project meets rigorous quality benchmarks and exceeds client expectations.</p>
        </div>
        <div class="strength-card">
            <div class="strength-icon"><i class="fas fa-bullseye"></i></div>
            <h3>Full-Spectrum Solutions</h3>
            <p>From concept to deployment and ongoing support, we handle every aspect of software development with specialized professionals.</p>
        </div>
        <div class="strength-card">
            <div class="strength-icon"><i class="fas fa-rocket"></i></div>
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

LOGIN_TEMPLATE = """
<div class="auth-page">
    <div class="auth-container">
        <div class="auth-left">
            <div class="auth-brand">
                <h1>MICROMATRIX</h1>
                <p class="auth-brand-tagline">INNOVATIVE</p>
            </div>
            <div class="auth-left-content">
                <h2>Welcome Back!</h2>
                <p>Login to access your Micromatrix account and manage your projects.</p>
                <div class="auth-features">
                    <div class="auth-feature"><i class="fas fa-check-circle"></i> Manage Projects</div>
                    <div class="auth-feature"><i class="fas fa-check-circle"></i> Track Orders</div>
                    <div class="auth-feature"><i class="fas fa-check-circle"></i> 24/7 Support</div>
                </div>
            </div>
        </div>
        <div class="auth-right">
            <div class="auth-card">
                <div class="auth-card-header">
                    <div class="auth-icon"><i class="fas fa-sign-in-alt"></i></div>
                    <h2>Login to Your Account</h2>
                    <p>Enter your credentials to continue</p>
                </div>
                {% if error %}
                <div class="auth-alert auth-alert-error">
                    <i class="fas fa-exclamation-circle"></i> {{ error }}
                </div>
                {% endif %}
                <form class="auth-form" method="POST" action="/login" id="loginForm">
                    <div class="auth-input-group">
                        <label for="login_email">Email Address</label>
                        <div class="auth-input-wrapper">
                            <i class="fas fa-envelope auth-input-icon"></i>
                            <input type="email" id="login_email" name="email" placeholder="your@email.com" required autocomplete="email">
                        </div>
                    </div>
                    <div class="auth-input-group">
                        <label for="login_password">Password</label>
                        <div class="auth-input-wrapper">
                            <i class="fas fa-lock auth-input-icon"></i>
                            <input type="password" id="login_password" name="password" placeholder="Your password" required autocomplete="current-password">
                            <button type="button" class="toggle-pwd" onclick="togglePassword('login_password', this)" tabindex="-1"><i class="fas fa-eye"></i></button>
                        </div>
                    </div>
                    <button type="submit" class="auth-submit-btn" id="loginBtn">
                        <span>Login</span> <i class="fas fa-arrow-right"></i>
                    </button>
                </form>
                <div class="auth-footer-link">
                    Don't have an account? <a href="/signup">Sign Up Here</a>
                </div>
            </div>
        </div>
    </div>
</div>
"""

SIGNUP_TEMPLATE = """
<div class="auth-page">
    <div class="auth-container">
        <div class="auth-left">
            <div class="auth-brand">
                <h1>MICROMATRIX</h1>
                <p class="auth-brand-tagline">INNOVATIVE</p>
            </div>
            <div class="auth-left-content">
                <h2>Join Micromatrix!</h2>
                <p>Create your account and start your digital transformation journey with us.</p>
                <div class="auth-features">
                    <div class="auth-feature"><i class="fas fa-check-circle"></i> Free Registration</div>
                    <div class="auth-feature"><i class="fas fa-check-circle"></i> Project Dashboard</div>
                    <div class="auth-feature"><i class="fas fa-check-circle"></i> Priority Support</div>
                </div>
            </div>
        </div>
        <div class="auth-right">
            <div class="auth-card">
                <div class="auth-card-header">
                    <div class="auth-icon"><i class="fas fa-user-plus"></i></div>
                    <h2>Create New Account</h2>
                    <p>Fill in the details below to get started</p>
                </div>
                {% if error %}
                <div class="auth-alert auth-alert-error">
                    <i class="fas fa-exclamation-circle"></i> {{ error }}
                </div>
                {% endif %}
                {% if success %}
                <div class="auth-alert auth-alert-success">
                    <i class="fas fa-check-circle"></i> {{ success }}
                </div>
                {% endif %}
                <form class="auth-form" method="POST" action="/signup" id="signupForm">
                    <div class="auth-input-group">
                        <label for="signup_username">Full Name / Username</label>
                        <div class="auth-input-wrapper">
                            <i class="fas fa-user auth-input-icon"></i>
                            <input type="text" id="signup_username" name="username" placeholder="Your name" required autocomplete="name" minlength="3">
                        </div>
                    </div>
                    <div class="auth-input-group">
                        <label for="signup_email">Email Address</label>
                        <div class="auth-input-wrapper">
                            <i class="fas fa-envelope auth-input-icon"></i>
                            <input type="email" id="signup_email" name="email" placeholder="your@email.com" required autocomplete="email">
                        </div>
                    </div>
                    <div class="auth-input-group">
                        <label for="signup_password">Password</label>
                        <div class="auth-input-wrapper">
                            <i class="fas fa-lock auth-input-icon"></i>
                            <input type="password" id="signup_password" name="password" placeholder="Min 6 characters" required minlength="6" autocomplete="new-password">
                            <button type="button" class="toggle-pwd" onclick="togglePassword('signup_password', this)" tabindex="-1"><i class="fas fa-eye"></i></button>
                        </div>
                    </div>
                    <div class="auth-input-group">
                        <label for="signup_confirm">Confirm Password</label>
                        <div class="auth-input-wrapper">
                            <i class="fas fa-lock auth-input-icon"></i>
                            <input type="password" id="signup_confirm" name="confirm_password" placeholder="Repeat password" required minlength="6" autocomplete="new-password">
                            <button type="button" class="toggle-pwd" onclick="togglePassword('signup_confirm', this)" tabindex="-1"><i class="fas fa-eye"></i></button>
                        </div>
                    </div>
                    <button type="submit" class="auth-submit-btn" id="signupBtn">
                        <span>Create Account</span> <i class="fas fa-arrow-right"></i>
                    </button>
                </form>
                <div class="auth-footer-link">
                    Already have an account? <a href="/login">Login Here</a>
                </div>
            </div>
        </div>
    </div>
</div>
"""

ADMIN_TEMPLATE = """
<div class="admin-page" style="padding: 2rem; max-width: 1400px; margin: 0 auto; background: var(--white-primary); min-height: 100vh;">
    <div class="admin-header" style="margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: center; background: linear-gradient(135deg, var(--navy-dark) 0%, var(--navy-primary) 100%); padding: 3rem; border-radius: 24px; color: white; box-shadow: var(--shadow-lg); border: 1px solid rgba(255,255,255,0.1);">
        <div>
            <h1 style="font-family: 'Outfit', sans-serif; font-weight: 900; letter-spacing: 3px; font-size: 2.5rem; margin-bottom: 0.5rem; background: linear-gradient(90deg, #fff 0%, var(--accent-violet) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">ADMIN DASHBOARD</h1>
            <p style="opacity: 0.9; font-size: 1.1rem; font-weight: 500;">Welcome back, Asif! Monitor your business performance here.</p>
        </div>
        <div class="admin-stats" style="display: flex; gap: 3rem;">
            <div class="stat-item" style="text-align: center; background: rgba(255,255,255,0.1); padding: 1.5rem 2rem; border-radius: 20px; backdrop-filter: blur(5px); border: 1px solid rgba(255,255,255,0.1);">
                <span style="display: block; font-size: 2.5rem; font-weight: 800; color: var(--accent-yellow);">{{ users_count }}</span>
                <span style="font-size: 0.85rem; text-transform: uppercase; opacity: 0.8; letter-spacing: 1px; font-weight: 700;">Total Users</span>
            </div>
            <div class="stat-item" style="text-align: center; background: rgba(255,255,255,0.1); padding: 1.5rem 2rem; border-radius: 20px; backdrop-filter: blur(5px); border: 1px solid rgba(255,255,255,0.1);">
                <span style="display: block; font-size: 2.5rem; font-weight: 800; color: var(--accent-blue);">{{ messages_count }}</span>
                <span style="font-size: 0.85rem; text-transform: uppercase; opacity: 0.8; letter-spacing: 1px; font-weight: 700;">Inquiries</span>
            </div>
        </div>
    </div>

    <div class="admin-grid" style="display: grid; grid-template-columns: 1fr; gap: 2.5rem;">
        <!-- Contact Messages Section -->
        <div class="admin-section" style="background: white; border-radius: 24px; padding: 2.5rem; box-shadow: var(--shadow-md); border: 1px solid var(--border-color);">
            <div style="display: flex; align-items: center; gap: 1.2rem; margin-bottom: 2rem;">
                <div style="width: 50px; height: 50px; background: linear-gradient(135deg, var(--accent-purple) 0%, var(--navy-primary) 100%); color: white; display: flex; align-items: center; justify-content: center; border-radius: 12px; font-size: 1.5rem; box-shadow: 0 8px 16px rgba(124,58,237,0.2);">
                    <i class="fas fa-envelope-open-text"></i>
                </div>
                <h2 style="font-family: 'Outfit', sans-serif; font-size: 1.8rem; color: var(--navy-primary);">Customer Inquiries & Orders</h2>
            </div>
            
            <div style="overflow-x: auto; border-radius: 15px; border: 1px solid var(--border-color);">
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="text-align: left; background: #f8faff; border-bottom: 2px solid var(--border-color);">
                            <th style="padding: 1.2rem; font-weight: 700; color: var(--navy-primary);">Date</th>
                            <th style="padding: 1.2rem; font-weight: 700; color: var(--navy-primary);">Customer Details</th>
                            <th style="padding: 1.2rem; font-weight: 700; color: var(--navy-primary);">Service Type</th>
                            <th style="padding: 1.2rem; font-weight: 700; color: var(--navy-primary);">Budget</th>
                            <th style="padding: 1.2rem; font-weight: 700; color: var(--navy-primary);">Message Content</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% if messages %}
                            {% for msg in messages %}
                            <tr style="border-bottom: 1px solid var(--border-color); transition: background 0.3s;" onmouseover="this.style.background='#f0f4ff'" onmouseout="this.style.background='transparent'">
                                <td style="padding: 1.2rem; font-size: 0.9rem; color: var(--text-light); white-space: nowrap;">{{ msg.created_at }}</td>
                                <td style="padding: 1.2rem;">
                                    <div style="font-weight: 700; color: var(--navy-primary);">{{ msg.name }}</div>
                                    <div style="font-size: 0.85rem; color: var(--accent-purple); font-weight: 600;">{{ msg.email }}</div>
                                    <div style="font-size: 0.85rem; color: var(--text-light);">{{ msg.phone }}</div>
                                </td>
                                <td style="padding: 1.2rem;"><span style="background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-teal) 100%); color: white; padding: 0.4rem 1rem; border-radius: 50px; font-size: 0.8rem; font-weight: 700; box-shadow: 0 4px 10px rgba(6,182,212,0.2);">{{ msg.service }}</span></td>
                                <td style="padding: 1.2rem; font-weight: 800; color: var(--success-color); font-size: 1rem;">{{ msg.budget }}</td>
                                <td style="padding: 1.2rem; font-size: 0.95rem; color: var(--text-dark); line-height: 1.5;">{{ msg.message }}</td>
                            </tr>
                            {% endfor %}
                        {% else %}
                            <tr>
                                <td colspan="5" style="padding: 4rem; text-align: center; color: var(--text-light); font-weight: 500;">
                                    <i class="fas fa-inbox" style="display: block; font-size: 3rem; margin-bottom: 1rem; opacity: 0.3;"></i>
                                    No inquiries found yet.
                                </td>
                            </tr>
                        {% endif %}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Users Section -->
        <div class="admin-section" style="background: white; border-radius: 24px; padding: 2.5rem; box-shadow: var(--shadow-md); border: 1px solid var(--border-color);">
            <div style="display: flex; align-items: center; gap: 1.2rem; margin-bottom: 2rem;">
                <div style="width: 50px; height: 50px; background: linear-gradient(135deg, var(--accent-blue) 0%, var(--navy-primary) 100%); color: white; display: flex; align-items: center; justify-content: center; border-radius: 12px; font-size: 1.5rem; box-shadow: 0 8px 16px rgba(6,182,212,0.2);">
                    <i class="fas fa-users"></i>
                </div>
                <h2 style="font-family: 'Outfit', sans-serif; font-size: 1.8rem; color: var(--navy-primary);">Registered Community</h2>
            </div>
            
            <div style="overflow-x: auto; border-radius: 15px; border: 1px solid var(--border-color);">
                <table style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="text-align: left; background: #f8faff; border-bottom: 2px solid var(--border-color);">
                            <th style="padding: 1.2rem; font-weight: 700; color: var(--navy-primary);">User ID</th>
                            <th style="padding: 1.2rem; font-weight: 700; color: var(--navy-primary);">Username</th>
                            <th style="padding: 1.2rem; font-weight: 700; color: var(--navy-primary);">Email Address</th>
                            <th style="padding: 1.2rem; font-weight: 700; color: var(--navy-primary);">Join Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for user in users %}
                        <tr style="border-bottom: 1px solid var(--border-color);">
                            <td style="padding: 1.2rem; color: var(--text-light); font-weight: 700;">#{{ user.id }}</td>
                            <td style="padding: 1.2rem; font-weight: 700; color: var(--navy-primary);">{{ user.username }}</td>
                            <td style="padding: 1.2rem; font-weight: 500;">{{ user.email }}</td>
                            <td style="padding: 1.2rem; font-size: 0.9rem; color: var(--text-light);">{{ user.created_at }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
"""

# =====================
# CSS CONTENT
# =====================

CSS_CONTENT = """
:root {
    --navy-primary: #1E1B4B;
    --navy-dark:    #0F0D2E;
    --navy-light:   #312E81;
    --white-primary:  #F8F7FF;
    --white-secondary: #FFFFFF;
    --accent-purple:  #7C3AED;
    --accent-violet:  #A78BFA;
    --accent-blue:    #06B6D4;
    --accent-teal:    #14B8A6;
    --accent-yellow:  #FBBF24;
    --accent-red:     #F43F5E;
    --accent-green:   #10B981;
    --text-dark:    #1E1B4B;
    --text-light:   #6B7280;
    --border-color: #E0E7FF;
    --success-color: #10B981;
    --error-color:  #F43F5E;
    --gradient-hero: linear-gradient(135deg, #0F0D2E 0%, #1E1B4B 40%, #312E81 75%, #1E40AF 100%);
    --gradient-card: linear-gradient(145deg, #ffffff 0%, #f0f4ff 100%);
    --shadow-glow: 0 0 30px rgba(124,58,237,0.25);
    --glass-bg: rgba(255, 255, 255, 0.7);
    --glass-border: rgba(255, 255, 255, 0.4);
}

/* Real-time Notification Toasts */
.notification-toast {
    position: fixed;
    bottom: 20px;
    left: 20px;
    background: white;
    padding: 1rem 1.5rem;
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    display: flex;
    align-items: center;
    gap: 1rem;
    z-index: 2000;
    transform: translateX(-150%);
    transition: transform 0.5s cubic-bezier(0.68, -0.55, 0.27, 1.55);
    border-left: 4px solid var(--accent-purple);
}

.notification-toast.active {
    transform: translateX(0);
}

.notif-icon {
    width: 40px;
    height: 40px;
    background: var(--navy-primary);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
}

.notif-content p {
    margin: 0;
    font-size: 0.9rem;
    color: var(--text-dark);
}

.notif-content span {
    font-size: 0.75rem;
    color: var(--text-light);
}

/* ---- Animated Logo ---- */
.logo-img-wrap {
    position: relative;
    width: 52px;
    height: 52px;
    flex-shrink: 0;
}

.logo-img {
    width: 52px;
    height: 52px;
    object-fit: contain;
    border-radius: 12px;
}

.animated-logo {
    animation: logo-float 3s ease-in-out infinite, logo-glow 3s ease-in-out infinite;
    filter: drop-shadow(0 0 8px rgba(161,130,221,0.8));
}

@keyframes logo-float {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-6px) rotate(3deg); }
}

@keyframes logo-glow {
    0%, 100% { filter: drop-shadow(0 0 6px rgba(161,130,221,0.7)); }
    50% { filter: drop-shadow(0 0 18px rgba(91,194,197,1)) drop-shadow(0 0 30px rgba(161,130,221,0.5)); }
}

.logo-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    cursor: pointer;
}

/* Custom Cursor Glow */
.cursor-glow {
    position: fixed;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(161,130,221,0.15) 0%, transparent 60%);
    border-radius: 50%;
    pointer-events: none;
    transform: translate(-50%, -50%);
    z-index: 9999;
    mix-blend-mode: screen;
    transition: width 0.3s, height 0.3s;
}

/* Live System Status */
.system-status {
    position: fixed;
    bottom: 20px;
    right: 90px; /* To not overlap chatbot */
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--navy-dark);
    display: flex;
    align-items: center;
    gap: 0.5rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    z-index: 1000;
    border: 1px solid var(--border-color);
}

.status-dot {
    width: 8px;
    height: 8px;
    background-color: var(--success-color);
    border-radius: 50%;
    animation: ping-pulse 1.5s infinite;
}

@keyframes ping-pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(91,194,197, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(91,194,197, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(91,194,197, 0); }
}

/* Global Clocks in Footer */
.global-clocks {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.1);
}

.clock-item {
    text-align: center;
}

.clock-item span {
    display: block;
    font-size: 0.75rem;
    color: var(--accent-purple);
    text-transform: uppercase;
    letter-spacing: 1px;
}

.clock-item strong {
    font-family: 'Outfit', sans-serif;
    font-size: 1.1rem;
    color: var(--white-primary);
}

/* Glassmorphism Effect */

.glass {
    background: var(--glass-bg) !important;
    backdrop-filter: blur(12px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(12px) saturate(180%) !important;
    border: 1px solid var(--glass-border) !important;
}

/* Animated Floating Blobs */
.blob {
    position: fixed;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(124,58,237,0.1) 0%, transparent 70%);
    border-radius: 50%;
    z-index: -1;
    filter: blur(50px);
    pointer-events: none;
    animation: blob-float 20s infinite alternate;
}

.blob-1 { top: -100px; left: -100px; animation-delay: 0s; }
.blob-2 { bottom: -100px; right: -100px; background: radial-gradient(circle, rgba(6,182,212,0.1) 0%, transparent 70%); animation-delay: -5s; }
.blob-3 { top: 40%; left: 30%; background: radial-gradient(circle, rgba(167,139,250,0.08) 0%, transparent 70%); animation-delay: -10s; }

@keyframes blob-float {
    from { transform: translate(0, 0) scale(1); }
    to { transform: translate(100px, 50px) scale(1.1); }
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
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background-color: var(--white-primary);
    color: var(--text-dark);
    line-height: 1.7;
    font-size: 1.05rem;
}

.header {
    background: linear-gradient(135deg, var(--navy-dark) 0%, var(--navy-primary) 60%, var(--navy-light) 100%);
    color: var(--white-primary);
    padding: 0.9rem 2rem;
    box-shadow: 0 4px 20px rgba(15,13,46,0.35);
    position: sticky;
    top: 0;
    z-index: 1000;
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(124,58,237,0.2);
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
    font-size: 1.6rem;
    margin: 0;
    letter-spacing: 3px;
    font-family: 'Outfit', sans-serif;
    font-weight: 900;
    background: linear-gradient(90deg, #fff 0%, var(--accent-violet) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.company-info p {
    font-size: 0.68rem;
    margin: 0;
    letter-spacing: 3px;
    color: var(--accent-violet);
    font-weight: 700;
    text-transform: uppercase;
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
    display: flex;
    flex-direction: column;
    background: none;
    border: none;
    cursor: pointer;
    gap: 6px;
    padding: 4px;
    z-index: 1100;
}

.menu-toggle .bar {
    width: 28px;
    height: 3px;
    background: var(--white-primary);
    border-radius: 3px;
    transition: all 0.35s ease;
    display: block;
}

.menu-toggle.open .bar1 {
    transform: translateY(9px) rotate(45deg);
}

.menu-toggle.open .bar2 {
    opacity: 0;
    transform: scaleX(0);
}

.menu-toggle.open .bar3 {
    transform: translateY(-9px) rotate(-45deg);
}

/* Sidebar */
.sidebar-overlay {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.55);
    z-index: 1050;
    transition: opacity 0.3s ease;
}

.sidebar-overlay.active {
    display: block;
}

/* Sidebar slides from RIGHT */
.sidebar {
    position: fixed;
    top: 0;
    right: -290px;
    left: auto;
    width: 270px;
    height: 100vh;
    background: #111111;
    z-index: 1100;
    transition: right 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: -4px 0 20px rgba(0,0,0,0.4);
    display: flex;
    flex-direction: column;
}

.sidebar.open {
    right: 0;
    left: auto;
}

.sidebar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 1.5rem 1rem;
    border-bottom: 1px solid #333;
    color: #fff;
    font-size: 0.85rem;
    letter-spacing: 3px;
    font-weight: 700;
}

.sidebar-close {
    background: none;
    border: none;
    color: #fff;
    font-size: 1.4rem;
    cursor: pointer;
    transition: color 0.3s;
}

.sidebar-close:hover {
    color: #aaa;
}

.sidebar-nav {
    display: flex;
    flex-direction: column;
    padding: 1rem 0;
}

.sidebar-link {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1.5rem;
    color: #dddddd;
    text-decoration: none;
    font-size: 1.1rem;
    font-weight: 500;
    border-left: 4px solid transparent;
    transition: all 0.3s ease;
}

.sidebar-link:hover {
    background: #222;
    color: #ffffff;
    border-left-color: #ffffff;
    padding-left: 2rem;
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
    background: url('/static/images/hero_bg.png') no-repeat center center;
    background-size: cover;
    color: var(--white-primary);
    padding: 6rem 2rem;
    margin-bottom: 3rem;
    position: relative;
    box-shadow: inset 0 0 0 2000px rgba(15, 13, 46, 0.75); /* Dark overlay */
}

.hero-badge {
    display: block;
    background: var(--accent-purple);
    color: #ffffff;
    padding: 0.8rem 1.5rem;
    border-radius: 20px;
    font-size: 0.95rem;
    margin-bottom: 2rem;
    letter-spacing: 1px;
    text-align: left;
}

.hero-content {
    background: linear-gradient(145deg, #ffffff 0%, #f0f4ff 100%);
    padding: 3rem;
    border-radius: 24px;
    box-shadow: 0 24px 70px rgba(30,27,75,0.14);
    border-left: 6px solid var(--accent-purple);
    display: flex;
    flex-direction: column;
    justify-content: center;
    color: var(--navy-primary);
    position: relative;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
}

.hero-content::before {
    content: '';
    position: absolute;
    top: -60px;
    right: -60px;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(124,58,237,0.1) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}

.hero-content h1 {
    font-size: 5rem;
    margin-bottom: 1.5rem;
    font-weight: 800;
    line-height: 1.1;
    text-align: center;
}

.hero-subtitle {
    font-size: 1.6rem;
    margin-bottom: 1rem;
    opacity: 0.95;
}

.hero-description {
    font-size: 1.25rem;
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
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.85rem 2.2rem;
    background: linear-gradient(135deg, var(--accent-purple) 0%, #5B21B6 100%);
    color: #ffffff;
    text-decoration: none;
    border-radius: 50px;
    font-weight: 700;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
    font-size: 0.95rem;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 15px rgba(124,58,237,0.35);
}

.cta-button:hover {
    background: linear-gradient(135deg, #6D28D9 0%, var(--accent-blue) 100%);
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(124,58,237,0.45);
}

.cta-button.secondary {
    background: transparent;
    border: 2px solid var(--accent-purple);
    color: var(--navy-primary);
    padding-left: 1.5rem;
    padding-right: 1.5rem;
    box-shadow: none;
}

.cta-button.secondary:hover {
    background: var(--accent-purple);
    color: #fff;
}

.cta-button-large {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 1rem 3rem;
    background: linear-gradient(135deg, var(--accent-purple) 0%, #1E40AF 100%);
    color: var(--white-primary);
    text-decoration: none;
    border-radius: 50px;
    font-weight: 700;
    transition: all 0.3s ease;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    box-shadow: 0 6px 20px rgba(124,58,237,0.4);
}

.cta-button-large:hover {
    background: linear-gradient(135deg, #6D28D9 0%, var(--accent-blue) 100%);
    transform: translateY(-3px);
    box-shadow: 0 16px 35px rgba(124,58,237,0.5);
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
    padding: 4rem 2rem;
    background: linear-gradient(180deg, var(--white-secondary) 0%, var(--white-primary) 100%);
    position: relative;
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
    font-size: 1.1rem;
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
    background: url('/static/images/services_bg.png') no-repeat center center;
    background-size: cover;
    color: var(--white-primary);
    padding: 5rem 2rem;
    text-align: center;
    position: relative;
    box-shadow: inset 0 0 0 2000px rgba(15, 13, 46, 0.78);
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
    padding: 5rem 2rem;
    background: url('/static/images/hero_bg.png') no-repeat center center;
    background-size: cover;
    margin-bottom: 2rem;
    border-radius: 32px;
    overflow: hidden;
    position: relative;
    box-shadow: inset 0 0 0 2000px rgba(15, 13, 46, 0.72);
    color: var(--white-primary);
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
.chatbot-messages {
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
        flex-direction: column;
        position: absolute;
        top: 100%;
        left: 0;
        width: 100%;
        background: var(--navy-primary);
        padding: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .navbar.active {
        display: flex;
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

/* =====================
   FOUNDER SECTION
   ===================== */
.founder-section {
    padding: 4rem 2rem;
    background: #f9f9f9;
}

.founder-card {
    display: flex;
    gap: 3rem;
    align-items: flex-start;
    max-width: 1100px;
    margin: 2rem auto 0;
    background: #fff;
    border-radius: 16px;
    padding: 3rem;
    box-shadow: 0 8px 40px rgba(0,0,0,0.09);
    border-left: 6px solid #111;
}

.founder-avatar {
    width: 120px;
    height: 120px;
    min-width: 120px;
    background: #111;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 3.5rem;
}

.founder-info h2 {
    font-size: 2.2rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    color: #111;
}

.founder-title, .founder-location, .founder-since {
    color: #555;
    margin-bottom: 0.4rem;
    font-size: 1rem;
}

.founder-title i, .founder-location i, .founder-since i {
    color: #111;
    margin-right: 0.4rem;
}

.founder-bio {
    margin: 1.2rem 0;
    color: #333;
    font-size: 1.1rem;
    line-height: 1.8;
}

.founder-stats {
    display: flex;
    gap: 2rem;
    margin: 1.5rem 0;
    flex-wrap: wrap;
}

.f-stat {
    text-align: center;
    background: #f4f4f4;
    padding: 0.8rem 1.2rem;
    border-radius: 8px;
    min-width: 80px;
}

.f-stat strong {
    display: block;
    font-size: 1.5rem;
    font-weight: 800;
    color: #111;
}

.f-stat span {
    font-size: 0.8rem;
    color: #777;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.founder-contact {
    display: flex;
    gap: 1.2rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}

.founder-link {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: #111;
    color: #fff;
    padding: 0.6rem 1.2rem;
    border-radius: 6px;
    text-decoration: none;
    font-size: 0.95rem;
    transition: background 0.3s ease;
}

.founder-link:hover {
    background: #333;
}

/* Founder mini card on home page */
.founder-mini-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: #f4f4f4;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 0.85rem 1.2rem;
    margin-top: 1.5rem;
    max-width: 420px;
}

.founder-mini-avatar {
    width: 44px;
    height: 44px;
    min-width: 44px;
    background: #111;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 1.3rem;
}

.founder-mini-tag {
    display: block;
    font-size: 0.85rem;
    color: #666;
    margin-top: 0.2rem;
}

@media (max-width: 768px) {
    .founder-card {
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .founder-contact {
        justify-content: center;
    }
    .founder-stats {
        justify-content: center;
    }
}


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
}

#micromatrix-text {
    color: #ffffff;
    background-color: var(--accent-blue);
    padding: 0.2rem 1.5rem;
    font-weight: 700;
    display: inline-block;
}

/* =====================
   NEW ANIMATIONS & EFFECTS
   ===================== */
#scroll-progress-bar {
    position: fixed;
    top: 0;
    left: 0;
    height: 4px;
    background: var(--navy-primary);
    width: 0%;
    z-index: 9999;
    transition: width 0.1s ease;
}

.ripple-btn {
    position: relative;
    overflow: hidden;
}

.ripple {
    position: absolute;
    border-radius: 50%;
    transform: scale(0);
    animation: ripple-anim 600ms linear;
    background-color: rgba(255, 255, 255, 0.4);
    pointer-events: none;
}

@keyframes ripple-anim {
    to {
        transform: scale(4);
        opacity: 0;
    }
}

.overview-card, .review-card, .service-card {
    will-change: transform;
    transform-style: preserve-3d;
}

/* =====================
   HEADER AUTH BUTTONS
   ===================== */
.nav-user {
    color: var(--accent-yellow);
    font-weight: 600;
    font-size: 0.95rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

.nav-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.45rem 1.1rem;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.9rem;
    text-decoration: none;
    transition: all 0.25s ease;
    border: 2px solid transparent;
}

.nav-btn-login {
    background: transparent;
    border-color: var(--accent-purple);
    color: var(--white-primary);
}

.nav-btn-login:hover {
    background: var(--accent-purple);
    color: #fff;
}

.nav-btn-signup {
    background: var(--accent-purple);
    color: #fff;
}

.nav-btn-signup:hover {
    background: var(--accent-blue);
    border-color: var(--accent-blue);
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(91,194,197,0.35);
}

.nav-btn-logout {
    background: transparent;
    border-color: var(--accent-red);
    color: var(--accent-red);
}

.nav-btn-logout:hover {
    background: var(--accent-red);
    color: #fff;
}

/* =====================
   AUTH PAGES
   ===================== */
.auth-page {
    min-height: calc(100vh - 80px);
    display: flex;
    align-items: stretch;
    background: var(--white-primary);
}

.auth-container {
    display: flex;
    width: 100%;
    min-height: 100%;
}

.auth-left {
    flex: 1;
    background: url('/static/images/auth_bg.png') no-repeat center center;
    background-size: cover;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 4rem 3rem;
    color: #fff;
    position: relative;
    overflow: hidden;
    box-shadow: inset 0 0 0 2000px rgba(15, 13, 46, 0.72);
}

.auth-left::before {
    content: '';
    position: absolute;
    top: -100px;
    right: -100px;
    width: 350px;
    height: 350px;
    border-radius: 50%;
    background: rgba(161, 130, 221, 0.15);
}

.auth-left::after {
    content: '';
    position: absolute;
    bottom: -80px;
    left: -80px;
    width: 250px;
    height: 250px;
    border-radius: 50%;
    background: rgba(91, 194, 197, 0.12);
}

.auth-brand h1 {
    font-size: 2.2rem;
    font-weight: 900;
    letter-spacing: 3px;
    color: #fff;
    margin-bottom: 0;
}

.auth-brand-tagline {
    font-size: 0.75rem;
    letter-spacing: 4px;
    color: var(--accent-purple);
    font-weight: 700;
    margin-bottom: 3rem;
}

.auth-left-content h2 {
    font-size: 2rem;
    margin-bottom: 1rem;
    color: #fff;
}

.auth-left-content p {
    color: rgba(255,255,255,0.8);
    font-size: 1rem;
    line-height: 1.7;
    margin-bottom: 2rem;
}

.auth-features {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}

.auth-feature {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    color: rgba(255,255,255,0.9);
    font-size: 1rem;
}

.auth-feature i {
    color: var(--accent-blue);
    font-size: 1.1rem;
}

.auth-right {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 3rem 2rem;
    background: var(--white-primary);
}

.auth-card {
    width: 100%;
    max-width: 480px;
    background: #fff;
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: 0 20px 60px rgba(42, 39, 93, 0.12);
    border: 1px solid var(--border-color);
}

.auth-card-header {
    text-align: center;
    margin-bottom: 2rem;
}

.auth-icon {
    width: 70px;
    height: 70px;
    background: linear-gradient(135deg, var(--navy-primary), var(--accent-purple));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1.2rem;
    font-size: 1.8rem;
    color: #fff;
    box-shadow: 0 8px 24px rgba(161, 130, 221, 0.4);
}

.auth-card-header h2 {
    font-size: 1.6rem;
    color: var(--navy-primary);
    margin-bottom: 0.3rem;
}

.auth-card-header p {
    color: var(--text-light);
    font-size: 0.95rem;
}

.auth-alert {
    padding: 0.85rem 1.2rem;
    border-radius: 8px;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 0.95rem;
    font-weight: 500;
}

.auth-alert-error {
    background: #fef2f2;
    color: #b91c1c;
    border: 1px solid #fecaca;
}

.auth-alert-success {
    background: #f0fdf4;
    color: #15803d;
    border: 1px solid #bbf7d0;
}

.auth-form {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
}

.auth-input-group label {
    display: block;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--navy-primary);
    margin-bottom: 0.4rem;
}

.auth-input-wrapper {
    position: relative;
    display: flex;
    align-items: center;
}

.auth-input-icon {
    position: absolute;
    left: 1rem;
    color: var(--text-light);
    font-size: 0.95rem;
    pointer-events: none;
    z-index: 1;
}

.auth-input-wrapper input {
    width: 100%;
    padding: 0.85rem 2.8rem;
    border: 2px solid var(--border-color);
    border-radius: 10px;
    font-size: 1rem;
    color: var(--text-dark);
    background: var(--white-primary);
    transition: all 0.25s ease;
    outline: none;
    font-family: inherit;
}

.auth-input-wrapper input:focus {
    border-color: var(--accent-purple);
    box-shadow: 0 0 0 3px rgba(161, 130, 221, 0.15);
    background: #fff;
}

.toggle-pwd {
    position: absolute;
    right: 0.8rem;
    background: none;
    border: none;
    cursor: pointer;
    color: var(--text-light);
    font-size: 0.95rem;
    padding: 0.3rem;
    transition: color 0.2s ease;
    z-index: 1;
}

.toggle-pwd:hover {
    color: var(--accent-purple);
}

.auth-submit-btn {
    width: 100%;
    padding: 0.95rem;
    background: linear-gradient(135deg, var(--navy-primary), var(--accent-purple));
    color: #fff;
    border: none;
    border-radius: 10px;
    font-size: 1.05rem;
    font-weight: 700;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.6rem;
    transition: all 0.3s ease;
    letter-spacing: 0.5px;
    margin-top: 0.5rem;
    font-family: inherit;
}

.auth-submit-btn:hover {
    background: linear-gradient(135deg, var(--accent-purple), var(--accent-blue));
    transform: translateY(-2px);
    box-shadow: 0 10px 28px rgba(161, 130, 221, 0.45);
}

.auth-footer-link {
    text-align: center;
    margin-top: 1.5rem;
    font-size: 0.95rem;
    color: var(--text-light);
}

.auth-footer-link a {
    color: var(--accent-purple);
    font-weight: 700;
    text-decoration: none;
    transition: color 0.2s ease;
}

.auth-footer-link a:hover {
    color: var(--navy-primary);
}

@media (max-width: 768px) {
    .auth-container { flex-direction: column; }
    .auth-left { padding: 2.5rem 1.5rem; min-height: 220px; }
    .auth-right { padding: 2rem 1rem; }
    .auth-card { padding: 1.8rem 1.2rem; }
    .nav-user, .nav-btn { font-size: 0.82rem; padding: 0.35rem 0.7rem; }
}

/* =====================
   RESPONSIVE NAVIGATION
   ===================== */

/* Desktop: show nav links, hide hamburger */
@media (min-width: 769px) {
    .menu-toggle {
        display: none !important;
    }
    .navbar {
        display: flex !important;
    }
}

/* Mobile: hide nav links, show hamburger on right */
@media (max-width: 768px) {
    .header-right {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-left: auto;
    }

    .navbar {
        display: none !important;
    }

    .menu-toggle {
        display: flex !important;
        flex-direction: column;
        justify-content: center;
        gap: 6px;
        background: none;
        border: 1.5px solid rgba(255,255,255,0.25);
        border-radius: 6px;
        cursor: pointer;
        padding: 6px 8px;
        z-index: 1100;
        margin-left: auto;
    }

    .menu-toggle .bar {
        width: 24px;
        height: 2.5px;
        background: var(--white-primary);
        border-radius: 3px;
        transition: all 0.35s ease;
        display: block;
    }

    .header-container {
        flex-wrap: nowrap;
    }

    .hero-title { font-size: 2rem; }
    .hero-subtitle { font-size: 1rem; }

    .footer-content {
        grid-template-columns: 1fr;
    }

    .services-grid,
    .overview-grid,
    .about-grid,
    .promise-grid {
        grid-template-columns: 1fr;
    }

    .section-header h2 { font-size: 1.8rem; }

    .chatbot-widget {
        bottom: 1rem;
        right: 1rem;
    }

    .chatbot-window {
        width: calc(100vw - 2rem);
        right: 0;
    }
}

@media (max-width: 480px) {
    .header { padding: 0.75rem 1rem; }
    .company-info h1 { font-size: 1.2rem; }
    .auth-left { display: none; }
    .auth-right { padding: 1.5rem 1rem; }
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

// =====================
// NAVIGATION TOGGLE - IMPROVED
// =====================

window.toggleMenu = function() {
    console.log('toggleMenu called');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    const menuToggle = document.getElementById('menuToggle');
    
    if (sidebar && overlay && menuToggle) {
        sidebar.classList.toggle('open');
        overlay.classList.toggle('active');
        menuToggle.classList.toggle('open');
        console.log('Sidebar state:', sidebar.classList.contains('open'));
    } else {
        console.error('Menu elements not found!');
    }
};

// =====================
// CHATBOT TOGGLE - IMPROVED
// =====================

window.chatbotOpen = false;
window.toggleChatbot = function() {
    console.log('toggleChatbot called');
    const widget = document.getElementById('chatbotWidget');
    if (widget) {
        window.chatbotOpen = !window.chatbotOpen;
        if (window.chatbotOpen) {
            widget.style.display = 'flex';
            widget.style.flexDirection = 'column';
            widget.style.visibility = 'visible';
            widget.style.opacity = '1';
            widget.classList.add('active');
        } else {
            widget.style.opacity = '0';
            setTimeout(() => {
                if (!window.chatbotOpen) {
                    widget.style.display = 'none';
                    widget.style.visibility = 'hidden';
                    widget.classList.remove('active');
                }
            }, 300);
        }
    } else {
        console.error('Chatbot widget not found!');
    }
};


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

// Chatbot functionality is now moved to the top for reliability

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
function togglePasswordVisibility(inputId, iconId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(iconId);
    if (input && icon) {
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
}

// 7. Handle Contact Form AJAX
async function handleContactForm(event) {
    event.preventDefault();
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn.innerHTML;
    
    // UI Loading State
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
    submitBtn.disabled = true;
    
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    try {
        const response = await fetch('/contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            alert('Success! ' + result.message);
            form.reset();
        } else {
            alert('Error: ' + result.message);
        }
    } catch (error) {
        console.error('Submission error:', error);
        alert('An unexpected error occurred. Please try again.');
    } finally {
        submitBtn.innerHTML = originalBtnText;
        submitBtn.disabled = false;
    }
}

// =====================
// REAL-TIME SOCIAL PROOF SYSTEM
// =====================

const socialProofData = [
    { city: 'London', action: 'purchased Web Development', icon: 'fa-globe' },
    { city: 'Dubai', action: 'ordered Mobile App', icon: 'fa-mobile-alt' },
    { city: 'New York', action: 'consulted for AI Solutions', icon: 'fa-robot' },
    { city: 'Islamabad', action: 'hired Remote Team', icon: 'fa-users' },
    { city: 'Berlin', action: 'ordered SEO Services', icon: 'fa-search' },
    { city: 'Singapore', action: 'purchased ERP System', icon: 'fa-cogs' },
    { city: 'Riyadh', action: 'started Fintech Project', icon: 'fa-credit-card' }
];

function showSocialProof() {
    const toast = document.getElementById('notificationToast');
    const msg = document.getElementById('notifMessage');
    const time = document.getElementById('notifTime');
    const icon = toast.querySelector('.notif-icon i');
    
    if (!toast) return;

    const data = socialProofData[Math.floor(Math.random() * socialProofData.length)];
    msg.innerHTML = `Someone from <strong>${data.city}</strong> ${data.action}!`;
    time.innerText = Math.floor(Math.random() * 5 + 1) + ' minutes ago';
    icon.className = `fas ${data.icon}`;

    toast.classList.add('active');
    
    setTimeout(() => {
        toast.classList.remove('active');
    }, 5000);
}

// Start social proof after 10 seconds
setTimeout(() => {
    showSocialProof();
    setInterval(showSocialProof, 20000); // Every 20 seconds
}, 10000);

// =====================
// LIVE VISITOR COUNTER
// =====================
function initVisitorCounter() {
    let count = Math.floor(Math.random() * 50) + 120;
    const footer = document.querySelector('.footer-bottom');
    if (footer) {
        const counterDiv = document.createElement('div');
        counterDiv.style.marginTop = '1rem';
        counterDiv.style.color = 'var(--accent-yellow)';
        counterDiv.style.fontWeight = '700';
        counterDiv.innerHTML = `<i class="fas fa-users"></i> <span id="liveCount">${count}</span> Visitors online right now`;
        footer.appendChild(counterDiv);

        setInterval(() => {
            count += Math.floor(Math.random() * 5) - 2;
            if (count < 100) count = 100;
            const display = document.getElementById('liveCount');
            if (display) display.innerText = count;
        }, 5000);
    }
}

document.addEventListener('DOMContentLoaded', initVisitorCounter);

// =====================
// NEW REAL-TIME EFFECTS
// =====================

// 1. Cursor Follower Glow
document.addEventListener('mousemove', (e) => {
    const cursor = document.getElementById('cursorGlow');
    if (cursor) {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    }
});

// Enlarge cursor glow on clickable elements
document.querySelectorAll('a, button, .service-card, .overview-card').forEach(el => {
    el.addEventListener('mouseenter', () => {
        const cursor = document.getElementById('cursorGlow');
        if (cursor) cursor.style.width = '450px';
        if (cursor) cursor.style.height = '450px';
    });
    el.addEventListener('mouseleave', () => {
        const cursor = document.getElementById('cursorGlow');
        if (cursor) cursor.style.width = '300px';
        if (cursor) cursor.style.height = '300px';
    });
});

// 2. Live Ping Simulator
function updatePing() {
    const pingEl = document.getElementById('statusPing');
    if (pingEl) {
        setInterval(() => {
            const ping = Math.floor(Math.random() * 15) + 8; // Random ping between 8ms and 22ms
            pingEl.innerHTML = `Systems Operational &bull; Ping: ${ping}ms`;
        }, 3000);
    }
}
document.addEventListener('DOMContentLoaded', updatePing);

// 3. Global Real-time Clocks
function updateGlobalClocks() {
    const now = new Date();
    
    // Formatting function
    const options = { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true };
    
    // Update New York
    const ny = document.getElementById('timeNY');
    if (ny) ny.innerText = new Intl.DateTimeFormat('en-US', { ...options, timeZone: 'America/New_York' }).format(now);
    
    // Update London
    const ldn = document.getElementById('timeLDN');
    if (ldn) ldn.innerText = new Intl.DateTimeFormat('en-US', { ...options, timeZone: 'Europe/London' }).format(now);
    
    // Update Dubai
    const dxb = document.getElementById('timeDXB');
    if (dxb) dxb.innerText = new Intl.DateTimeFormat('en-US', { ...options, timeZone: 'Asia/Dubai' }).format(now);
    
    // Update Islamabad
    const isb = document.getElementById('timeISB');
    if (isb) isb.innerText = new Intl.DateTimeFormat('en-US', { ...options, timeZone: 'Asia/Karachi' }).format(now);
}

// Start clocks if elements exist
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('globalClocks')) {
        updateGlobalClocks();
        setInterval(updateGlobalClocks, 1000); // Update every second
    }
});

"""

# =====================
# FLASK ROUTES
# =====================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id') or session.get('email') != 'asifhavelilakha@gmail.com':
            flash('Access denied. Administrator only.', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if session.get('user_id'):
        if session.get('email') == 'asifhavelilakha@gmail.com':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get users
        cursor.execute('SELECT id, username, email, created_at FROM users ORDER BY created_at DESC')
        users = cursor.fetchall()
        
        # Get messages
        cursor.execute('SELECT * FROM messages ORDER BY created_at DESC')
        messages = cursor.fetchall()
        
        users_count = len(users)
        messages_count = len(messages)
        
    html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', 
        render_template_string(ADMIN_TEMPLATE, users=users, messages=messages, 
                              users_count=users_count, messages_count=messages_count))
    html = render_template_string(html, css_content=CSS_CONTENT, js_content=JS_CONTENT)
    return html

@app.route('/home')
@login_required
def home():
    content = render_template_string(HOME_TEMPLATE, reviews=reviews)
    html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content)
    html = render_template_string(html, css_content=CSS_CONTENT, js_content=JS_CONTENT)
    return html

@app.route('/services')
@login_required
def services():
    content = render_template_string(SERVICES_TEMPLATE, services=services_data, pricing=pricing_data)
    html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', content)
    html = render_template_string(html, css_content=CSS_CONTENT, js_content=JS_CONTENT)
    return html

@app.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    if request.method == 'POST':
        try:
            # Handle both JSON and Form data
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form
            
            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone', 'N/A')
            service = data.get('service', 'General Inquiry')
            budget = data.get('budget', 'Not Specified')
            message = data.get('message')
            
            # 1. Save to Database
            with sqlite3.connect(DB_NAME) as conn:
                conn.execute('''
                    INSERT INTO messages (name, email, phone, service, budget, message)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, email, phone, service, budget, message))
                conn.commit()
            
            # 2. Send Email Alert to Admin
            try:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                subject = f"New Project Order: {service} from {name}"
                body = f"""
NEW ORDER / INQUIRY RECEIVED

Client Details:
---------------
Name: {name}
Email: {email}
Phone: {phone}
Service: {service}
Budget: {budget}
Time: {timestamp}

Message:
--------
{message}

---
This is an automated notification from your Micromatrix Admin Panel.
                """
                msg = Message(subject=subject,
                             recipients=[OWNER_EMAIL],
                             body=body)
                mail.send(msg)
            except Exception as e:
                print(f"Email sending failed: {str(e)}")
            
            if request.is_json:
                return jsonify({'status': 'success', 'message': 'Order submitted successfully! We will contact you soon.'})
            else:
                flash('Your inquiry has been sent successfully!', 'success')
                return redirect(url_for('contact'))
                
        except Exception as e:
            print(f"Error in contact: {str(e)}")
            if request.is_json:
                return jsonify({'status': 'error', 'message': 'There was an error. Please try again.'}), 500
            else:
                flash('An error occurred. Please try again.', 'error')
                return redirect(url_for('contact'))
    
    html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}', render_template_string(CONTACT_TEMPLATE, pricing=pricing_data))
    html = render_template_string(html, css_content=CSS_CONTENT, js_content=JS_CONTENT)
    return html


@app.route('/about')
@login_required
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

    # Step 1: Exact match
    if user_message in chatbot_knowledge:
        return jsonify({'response': chatbot_knowledge[user_message]})

    # Step 2: Key is contained in user message or user message contains key
    for key, value in chatbot_knowledge.items():
        if key in user_message or user_message in key:
            return jsonify({'response': value})

    # Step 3: Keyword-based matching (smarter fuzzy)
    keyword_map = {
        ('service', 'offer', 'do', 'provide', 'work', 'speciali'): 'what services do you offer',
        ('contact', 'reach', 'phone', 'call', 'whatsapp', 'number'): 'how can i contact you',
        ('email', 'mail', 'inbox'): 'what is your email',
        ('price', 'cost', 'fee', 'charge', 'budget', 'rate', 'how much'): 'pricing',
        ('remote', 'office', 'location', 'where', 'based', 'country'): 'what is your location',
        ('founder', 'owner', 'ceo', 'who lead', 'started', 'created', 'asif'): 'founder',
        ('support', '24/7', 'help', 'assist'): 'do you provide support',
        ('ai', 'machine learning', 'artificial', 'ml', 'data', 'deep'): 'what technology do you use',
        ('experience', 'year', 'portfolio', 'project'): 'do you have experience',
        ('hello', 'hey', 'salam', 'salaam', 'assalam', 'hola'): 'hello',
        ('hi', 'hiya', 'howdy'): 'hi',
        ('thank', 'shukriya', 'shukria'): 'thank you',
        ('process', 'method', 'approach', 'how you work', 'procedure'): 'process',
        ('tech', 'stack', 'language', 'framework', 'tool'): 'what technology do you use',
        ('about', 'micromatrix', 'company', 'firm', 'business'): 'what is micromatrix',
        ('start', 'begin', 'initiate', 'project', 'discuss'): 'can you help with my project',
    }
    for keywords, knowledge_key in keyword_map.items():
        for kw in keywords:
            if kw in user_message:
                return jsonify({'response': chatbot_knowledge.get(knowledge_key, '')})

    default_response = (
        "That's an interesting question! "
        "For detailed information, you can reach our team directly:\n"
        "📞 Phone: +923316170980\n"
        "📧 Email: info@micromatrix.tech\n"
        "💬 WhatsApp: wa.me/923316170980\n"
        "Or visit our Services or Contact page for more details."
    )
    return jsonify({'response': default_response})

# =====================
# AUTH ROUTES
# =====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('home'))
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        if not email or not password:
            error = 'Please fill in all fields.'
        else:
            with sqlite3.connect(DB_NAME) as conn:
                conn.row_factory = sqlite3.Row
                user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['email'] = user['email']
                return redirect(url_for('home'))
            else:
                error = 'Invalid email or password. Please try again.'
    html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}',
        render_template_string(LOGIN_TEMPLATE, error=error))
    html = render_template_string(html, css_content=CSS_CONTENT, js_content=JS_CONTENT)
    return html

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if session.get('user_id'):
        return redirect(url_for('home'))
    error = None
    success = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        if not username or not email or not password or not confirm:
            error = 'Please fill in all fields.'
        elif len(username) < 3:
            error = 'Username must be at least 3 characters.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters.'
        elif password != confirm:
            error = 'Passwords do not match. Please try again.'
        else:
            try:
                pw_hash = generate_password_hash(password)
                with sqlite3.connect(DB_NAME) as conn:
                    conn.execute(
                        'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                        (username, email, pw_hash)
                    )
                    conn.commit()
                success = 'Account created successfully! You can now login.'
            except sqlite3.IntegrityError as e:
                if 'email' in str(e):
                    error = 'An account with this email already exists.'
                elif 'username' in str(e):
                    error = 'This username is already taken. Please choose another.'
                else:
                    error = 'Registration failed. Please try again.'
    html = BASE_TEMPLATE.replace('{% block content %}{% endblock %}',
        render_template_string(SIGNUP_TEMPLATE, error=error, success=success))
    html = render_template_string(html, css_content=CSS_CONTENT, js_content=JS_CONTENT)
    return html

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

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
