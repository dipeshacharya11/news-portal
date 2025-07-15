# 📰 News Portal Django

A professional news portal built with Django featuring real-time news updates from NewsData.io API, comprehensive category management, responsive NBC News-style design, and advanced content management system.

![News Portal](https://img.shields.io/badge/Django-5.x-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

## ✨ Features

### 🚀 Core Features
- **Real-time News Updates** from NewsData.io API (200 requests/hour, 1000/day)
- **Responsive Design** with NBC News-style layout
- **Category Management** with 12+ news categories (Politics, Technology, Sports, etc.)
- **Breaking News Alerts** with animated indicators and live updates
- **Featured & Trending News** sections with priority-based display
- **Advanced Search** functionality across all content
- **User Authentication** and comprehensive profile management
- **Comment System** for user engagement and discussions
- **Newsletter Subscription** system with email notifications
- **Advertisement Management** system with multiple ad placements

### 📡 API Integration
- **NewsData.io Integration** for live news feeds from global sources
- **Automated News Fetching** with Django management commands
- **Smart Rate Limiting** and caching for optimal API usage
- **Multiple News Sources** aggregation and deduplication
- **Real-time Breaking News** alerts with priority handling
- **Category-based Fetching** for targeted content updates

### 🎨 Design & User Experience
- **Modern Responsive Design** optimized for desktop, tablet, and mobile
- **Professional Layout** inspired by major news websites (NBC News style)
- **Interactive Elements** with smooth CSS animations and hover effects
- **Enhanced News Hierarchy** with priority-based content organization
- **Fast Loading** with optimized assets and lazy loading
- **SEO Optimized** structure with meta tags and structured data

### 🔧 Admin & Management
- **Custom Admin Panel** for comprehensive content management
- **News API Management** dashboard with real-time monitoring
- **Analytics Dashboard** with statistics and user engagement metrics
- **User Management** system with role-based permissions
- **Advertisement Management** tools for revenue optimization
- **Database Backup** system with automated and manual options

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** (recommended: Python 3.10+)
- **pip** package manager
- **Git** for version control
- **NewsData.io API Key** (free tier: 200 requests/hour)

### 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dipeshacharya11/news-portal.git
   cd news-portal
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env file with your settings
   NEWSDATA_API_KEY=your-newsdata-api-key-here
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

5. **Set up the database:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Collect static files:**
   ```bash
   python manage.py collectstatic
   ```

### 🏃‍♂️ Running the Project

1. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

2. **Access the application:**
   - **Homepage:** http://127.0.0.1:8000/
   - **Admin Panel:** http://127.0.0.1:8000/admin/
   - **Custom Admin:** http://127.0.0.1:8000/custom-admin/
   - **API Management:** http://127.0.0.1:8000/custom-admin/news-api/

### 📡 NewsData.io API Setup

1. **Get your API key:**
   - Visit [NewsData.io](https://newsdata.io/)
   - Sign up for a free account
   - Copy your API key from the dashboard

2. **Configure the API:**
   ```bash
   # Add to your .env file
   NEWSDATA_API_KEY=pub_your_api_key_here
   DEFAULT_NEWS_CATEGORIES=top,politics,technology,business,sports,world,health
   DEFAULT_NEWS_LANGUAGE=en
   DEFAULT_NEWS_COUNTRY=us
   ```

3. **Fetch your first news:**
   ```bash
   # Fetch breaking news
   python manage.py fetch_news --breaking-only

   # Fetch technology news
   python manage.py fetch_news --category=technology --size=10

   # Fetch all categories
   python manage.py fetch_news --size=50
   ```

## Folder Structure
- `account/` - User accounts and authentication
- `comment/` - Comments system
- `core/` - Project settings and configuration
- `custom_admin/` - Custom admin views
- `mainsite/` - Main site logic
- `news/` - News aggregation and management
- `subscription/` - Subscription management
- `media/` - Uploaded files
- `static/` - Static assets
- `templates/` - HTML templates

## Environment Variables
See `.env` for all configuration options. **Do not commit sensitive data to public repos.**

## License
MIT

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 👨‍💻 Author

**Dipesh Acharya**
- GitHub: [@dipeshacharya11](https://github.com/dipeshacharya11)
- Repository: [news-portal](https://github.com/dipeshacharya11/news-portal)

## 🙏 Acknowledgments

- [NewsData.io](https://newsdata.io/) for providing the news API
- [Django](https://djangoproject.com/) for the excellent web framework
- [Bootstrap](https://getbootstrap.com/) for responsive design components
- [Font Awesome](https://fontawesome.com/) for beautiful icons

---

**⭐ If you find this project helpful, please give it a star on GitHub!**
