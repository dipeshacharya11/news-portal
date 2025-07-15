// Modern News Portal JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeAds();
    initializeSearch();
    initializeNewsletterSubscription();
    initializeLazyLoading();
    initializeReadingProgress();
    initializeDarkMode();
    
    // Auto-refresh breaking news and latest updates
    setInterval(checkBreakingNews, 60000); // Check every minute
    setInterval(updateLatestNews, 120000); // Update every 2 minutes
    initializeNewsHierarchy();
});

// Advertisement System
function initializeAds() {
    loadBannerAds();
    loadSidebarAds();
    
    // Track ad impressions when they come into view
    const adElements = document.querySelectorAll('[data-ad-id]');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const adId = entry.target.dataset.adId;
                if (adId && !entry.target.dataset.impressionTracked) {
                    trackAdImpression(adId);
                    entry.target.dataset.impressionTracked = 'true';
                }
            }
        });
    }, { threshold: 0.5 });
    
    adElements.forEach(el => observer.observe(el));
}

function loadBannerAds() {
    const bannerSlots = document.querySelectorAll('#banner-ad-1, #banner-ad-2');
    
    bannerSlots.forEach(slot => {
        fetch('/api/ads/banner/')
            .then(response => response.json())
            .then(data => {
                if (data.success && data.ad) {
                    displayAd(slot, data.ad);
                }
            })
            .catch(error => console.error('Error loading banner ad:', error));
    });
}

function loadSidebarAds() {
    const sidebarSlots = document.querySelectorAll('#sidebar-ad-1, #sidebar-ad-2');
    
    sidebarSlots.forEach(slot => {
        fetch('/api/ads/sidebar/')
            .then(response => response.json())
            .then(data => {
                if (data.success && data.ad) {
                    displayAd(slot, data.ad);
                }
            })
            .catch(error => console.error('Error loading sidebar ad:', error));
    });
}

function displayAd(container, ad) {
    let adContent = '';
    
    if (ad.html_content) {
        adContent = ad.html_content;
    } else if (ad.image) {
        adContent = `
            <div class="ad-content" data-ad-id="${ad.id}">
                <img src="${ad.image}" alt="${ad.title}" 
                     class="img-fluid ad-image" 
                     onclick="trackAdClick(${ad.id}, '${ad.url}')"
                     style="cursor: pointer; border-radius: 8px;">
                <small class="text-muted d-block mt-1">Advertisement</small>
            </div>
        `;
    }
    
    container.innerHTML = adContent;
    container.dataset.adId = ad.id;
}

// Search Functionality
function initializeSearch() {
    const searchForm = document.querySelector('form[role="search"]');
    const searchInput = document.querySelector('input[type="search"]');
    
    if (searchInput) {
        // Live search suggestions
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                if (this.value.length > 2) {
                    fetchSearchSuggestions(this.value);
                }
            }, 300);
        });
    }
}

function fetchSearchSuggestions(query) {
    fetch(`/api/search/suggestions/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            displaySearchSuggestions(data.suggestions);
        })
        .catch(error => console.error('Error fetching search suggestions:', error));
}

function displaySearchSuggestions(suggestions) {
    // Implementation for search suggestions dropdown
    console.log('Search suggestions:', suggestions);
}

// Newsletter Subscription
function initializeNewsletterSubscription() {
    const newsletterForms = document.querySelectorAll('.newsletter-form');
    
    newsletterForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = this.querySelector('input[type="email"]').value;
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            
            submitBtn.textContent = 'Subscribing...';
            submitBtn.disabled = true;
            
            fetch('/api/newsletter/subscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify({ email: email })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Successfully subscribed to newsletter!', 'success');
                    this.reset();
                } else {
                    showNotification(data.message || 'Subscription failed', 'error');
                }
            })
            .catch(error => {
                showNotification('An error occurred. Please try again.', 'error');
            })
            .finally(() => {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            });
        });
    });
}

// Lazy Loading for Images
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Reading Progress Bar
function initializeReadingProgress() {
    const progressBar = document.createElement('div');
    progressBar.className = 'reading-progress';
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        z-index: 9999;
        transition: width 0.3s ease;
    `;
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset;
        const docHeight = document.body.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;
        progressBar.style.width = scrollPercent + '%';
    });
}

// Dark Mode Toggle
function initializeDarkMode() {
    const darkModeToggle = document.createElement('button');
    darkModeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    darkModeToggle.className = 'btn btn-outline-secondary btn-sm position-fixed';
    darkModeToggle.style.cssText = 'bottom: 20px; right: 20px; z-index: 1000; border-radius: 50%; width: 50px; height: 50px;';
    
    darkModeToggle.addEventListener('click', toggleDarkMode);
    document.body.appendChild(darkModeToggle);
    
    // Check for saved dark mode preference
    if (localStorage.getItem('darkMode') === 'enabled') {
        enableDarkMode();
    }
}

function toggleDarkMode() {
    if (document.body.classList.contains('dark-mode')) {
        disableDarkMode();
    } else {
        enableDarkMode();
    }
}

function enableDarkMode() {
    document.body.classList.add('dark-mode');
    localStorage.setItem('darkMode', 'enabled');

    // Update toggle button icons
    const navToggle = document.getElementById('darkModeToggle');
    const floatingToggle = document.querySelector('button[style*="bottom: 20px"]');

    if (navToggle) {
        navToggle.innerHTML = '<i class="fas fa-sun me-1"></i><span class="d-none d-lg-inline">Light</span>';
    }
    if (floatingToggle) {
        floatingToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }

    // Add comprehensive dark mode styles
    if (!document.getElementById('dark-mode-styles')) {
        const darkStyles = document.createElement('style');
        darkStyles.id = 'dark-mode-styles';
        darkStyles.textContent = `
            /* Dark Mode Base */
            .dark-mode {
                background-color: #1a1a1a !important;
                color: #e5e5e5 !important;
            }

            /* Navigation */
            .dark-mode .navbar-modern {
                background-color: #2d2d2d !important;
                border-bottom: 1px solid #404040 !important;
            }

            .dark-mode .navbar-nav .nav-link {
                color: #e5e5e5 !important;
            }

            .dark-mode .navbar-nav .nav-link:hover {
                color: #0078d4 !important;
            }

            /* Brand Styling in Dark Mode */
            .dark-mode .brand-main {
                color: #0078d4 !important;
            }

            .dark-mode .brand-sub {
                color: #d13438 !important;
            }

            /* Cards and Containers */
            .dark-mode .card, .dark-mode .news-card,
            .dark-mode .hero-card, .dark-mode .main-story-card,
            .dark-mode .secondary-story-card, .dark-mode .sub-news-section,
            .dark-mode .live-section, .dark-mode .latest-news-section,
            .dark-mode .category-sidebar, .dark-mode .tech-sidebar {
                background-color: #2d2d2d !important;
                color: #e5e5e5 !important;
                border: 1px solid #404040 !important;
            }

            /* Text Colors */
            .dark-mode h1, .dark-mode h2, .dark-mode h3,
            .dark-mode h4, .dark-mode h5, .dark-mode h6,
            .dark-mode .main-story-title, .dark-mode .section-title,
            .dark-mode .category-title, .dark-mode .secondary-story-title,
            .dark-mode .sub-news-title, .dark-mode .live-title,
            .dark-mode .latest-news-title, .dark-mode .category-story-title,
            .dark-mode .sidebar-title, .dark-mode .related-story-title,
            .dark-mode .tech-story-title, .dark-mode .trending-tech-title {
                color: #e5e5e5 !important;
            }

            .dark-mode .main-story-title a, .dark-mode .section-title a,
            .dark-mode .category-title a, .dark-mode .secondary-story-title a,
            .dark-mode .sub-news-title a, .dark-mode .live-title a,
            .dark-mode .latest-news-title a, .dark-mode .category-story-title a,
            .dark-mode .related-story-title a, .dark-mode .tech-story-title a,
            .dark-mode .trending-tech-title a {
                color: #e5e5e5 !important;
            }

            .dark-mode .main-story-title a:hover, .dark-mode .section-title a:hover,
            .dark-mode .category-title a:hover, .dark-mode .secondary-story-title a:hover,
            .dark-mode .sub-news-title a:hover, .dark-mode .live-title a:hover,
            .dark-mode .latest-news-title a:hover, .dark-mode .category-story-title a:hover,
            .dark-mode .related-story-title a:hover, .dark-mode .tech-story-title a:hover,
            .dark-mode .trending-tech-title a:hover {
                color: #0078d4 !important;
            }

            /* Meta Text */
            .dark-mode .story-meta, .dark-mode .secondary-story-meta,
            .dark-mode .sub-news-meta, .dark-mode .latest-news-meta,
            .dark-mode .text-muted {
                color: #9ca3af !important;
            }

            /* Excerpts and Descriptions */
            .dark-mode .main-story-excerpt, .dark-mode .story-excerpt,
            .dark-mode .news-excerpt {
                color: #b3b3b3 !important;
            }

            /* Borders and Lines */
            .dark-mode .category-line, .dark-mode .section-title {
                border-color: #0078d4 !important;
            }

            /* Buttons */
            .dark-mode .btn-modern {
                background-color: #0078d4 !important;
                border-color: #0078d4 !important;
            }

            .dark-mode .btn-outline-secondary {
                border-color: #404040 !important;
                color: #e5e5e5 !important;
            }

            .dark-mode .btn-outline-secondary:hover {
                background-color: #404040 !important;
                color: #e5e5e5 !important;
            }

            /* Tags and Badges */
            .dark-mode .tag-badge {
                background-color: #404040 !important;
                color: #e5e5e5 !important;
            }

            .dark-mode .breaking-badge {
                background-color: #d13438 !important;
            }

            /* Footer */
            .dark-mode .footer-modern {
                background-color: #0f0f0f !important;
                border-top: 1px solid #404040 !important;
            }

            /* Forms */
            .dark-mode .form-control {
                background-color: #404040 !important;
                border-color: #555 !important;
                color: #e5e5e5 !important;
            }

            .dark-mode .form-control:focus {
                background-color: #404040 !important;
                border-color: #0078d4 !important;
                color: #e5e5e5 !important;
                box-shadow: 0 0 0 0.2rem rgba(0, 120, 212, 0.25) !important;
            }

            /* Dropdown Menus */
            .dark-mode .dropdown-menu {
                background-color: #2d2d2d !important;
                border-color: #404040 !important;
            }

            .dark-mode .dropdown-item {
                color: #e5e5e5 !important;
            }

            .dark-mode .dropdown-item:hover {
                background-color: #404040 !important;
                color: #e5e5e5 !important;
            }
        `;
        document.head.appendChild(darkStyles);
    }
}

function disableDarkMode() {
    document.body.classList.remove('dark-mode');
    localStorage.setItem('darkMode', null);

    // Update toggle button icons
    const navToggle = document.getElementById('darkModeToggle');
    const floatingToggle = document.querySelector('button[style*="bottom: 20px"]');

    if (navToggle) {
        navToggle.innerHTML = '<i class="fas fa-moon me-1"></i><span class="d-none d-lg-inline">Dark</span>';
    }
    if (floatingToggle) {
        floatingToggle.innerHTML = '<i class="fas fa-moon"></i>';
    }
}

// Enhanced Breaking News Check
function checkBreakingNews() {
    // Check multiple API endpoints for breaking news
    Promise.all([
        fetch('/api/breaking-news/').then(response => response.json()).catch(() => null),
        fetch('/api/newsdata/breaking/').then(response => response.json()).catch(() => null),
        fetch('/api/homepage/').then(response => response.json()).catch(() => null)
    ])
    .then(([mainApiData, newsDataApi, homepageData]) => {
        let breakingNews = [];

        // Priority 1: Get breaking news from main API
        if (mainApiData && mainApiData.status === 'success' && mainApiData.breaking_news) {
            breakingNews = mainApiData.breaking_news;
        }

        // Priority 2: Get breaking news from NewsData API
        if (breakingNews.length === 0 && newsDataApi && newsDataApi.status === 'success' && newsDataApi.breaking_news) {
            breakingNews = newsDataApi.breaking_news;
        }

        // Priority 3: Fallback to homepage breaking news
        if (breakingNews.length === 0 && homepageData && homepageData.breaking_news_items) {
            breakingNews = homepageData.breaking_news_items.slice(0, 5);
        }

        if (breakingNews.length > 0) {
            updateBreakingNewsBanner(breakingNews);
            showBreakingNewsBanner();
            console.log('Breaking news updated:', breakingNews.length, 'items');
        } else {
            console.log('No breaking news found');
        }
    })
    .catch(error => {
        console.error('Error checking breaking news:', error);
        // Fallback to static breaking news if available
        checkStaticBreakingNews();
    });
}

function updateBreakingNewsBanner(breakingNews) {
    const banner = document.querySelector('.breaking-news-modern');
    if (banner) {
        const ticker = banner.querySelector('.breaking-ticker');
        if (ticker) {
            ticker.innerHTML = breakingNews.map(news => {
                const title = news.title || news.headline || 'Breaking News';
                const content = news.content || news.description || news.excerpt || '';
                const truncatedContent = content.substring(0, 80);

                return `<div class="breaking-item">
                    <span class="breaking-title">${title}</span>
                    ${truncatedContent ? `<span class="breaking-desc">${truncatedContent}...</span>` : ''}
                </div>`;
            }).join('');

            // Restart animation
            ticker.style.animation = 'none';
            ticker.offsetHeight; // Trigger reflow
            ticker.style.animation = 'breakingScroll 35s linear infinite';
        }
    }
}

function showBreakingNewsBanner() {
    const banner = document.querySelector('.breaking-news-modern');
    if (banner) {
        banner.style.display = 'block';
        banner.style.opacity = '1';
        banner.style.transform = 'translateY(0)';

        // Start ticker animation
        const ticker = banner.querySelector('.breaking-ticker');
        if (ticker && ticker.children.length > 0) {
            ticker.style.animation = 'breakingScroll 35s linear infinite';
        }
    }
}

function checkStaticBreakingNews() {
    // Check if there are any breaking news items already on the page
    const existingBreaking = document.querySelectorAll('[data-breaking="true"]');
    if (existingBreaking.length > 0) {
        const breakingData = Array.from(existingBreaking).map(item => {
            // Try to extract title and content from different possible structures
            let title = 'Breaking News';
            let content = '';

            // Check for title in various elements
            const titleElement = item.querySelector('.breaking-title, .news-title, .story-title, h3, h4, strong');
            if (titleElement) {
                title = titleElement.textContent.trim();
            }

            // Check for content in various elements
            const contentElement = item.querySelector('.breaking-desc, .news-excerpt, .story-excerpt, p');
            if (contentElement) {
                content = contentElement.textContent.trim();
            }

            return { title, content };
        });

        updateBreakingNewsBanner(breakingData);
        showBreakingNewsBanner();
    }
}

// Utility Functions
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Social Media Sharing
function shareArticle(url, title, platform) {
    const shareUrls = {
        facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`,
        twitter: `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`,
        linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`,
        whatsapp: `https://wa.me/?text=${encodeURIComponent(title + ' ' + url)}`
    };
    
    if (shareUrls[platform]) {
        window.open(shareUrls[platform], '_blank', 'width=600,height=400');
    }
}

// News Hierarchy and Real-time Updates
function initializeNewsHierarchy() {
    // Add priority indicators
    addPriorityIndicators();

    // Initialize live updates
    startLiveIndicator();

    // Add hover effects for news items
    addNewsItemInteractions();
}

function addPriorityIndicators() {
    const newsItems = document.querySelectorAll('.latest-news-item');
    newsItems.forEach(item => {
        const priorityBadge = item.querySelector('.priority-badge');
        if (priorityBadge) {
            item.classList.add('has-priority');

            // Add click tracking
            item.addEventListener('click', function() {
                trackNewsClick(item);
            });
        }
    });
}

function startLiveIndicator() {
    const liveIndicator = document.querySelector('.live-indicator');
    if (liveIndicator) {
        // Add pulsing effect
        setInterval(() => {
            liveIndicator.style.opacity = '0.7';
            setTimeout(() => {
                liveIndicator.style.opacity = '1';
            }, 500);
        }, 2000);
    }
}

function addNewsItemInteractions() {
    const newsItems = document.querySelectorAll('.latest-news-item, .sub-news-item, .trending-item');

    newsItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(5px)';
            this.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.1)';
        });

        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
            this.style.boxShadow = 'none';
        });
    });
}

function updateLatestNews() {
    // Simulate real-time updates (in production, this would fetch from API)
    const updateCount = document.querySelector('.update-count');
    if (updateCount) {
        const currentCount = parseInt(updateCount.textContent.match(/\d+/)[0]);
        const newCount = currentCount + Math.floor(Math.random() * 3);
        updateCount.textContent = `${newCount} new`;

        // Add notification animation
        updateCount.style.animation = 'pulse 0.5s ease-in-out';
        setTimeout(() => {
            updateCount.style.animation = '';
        }, 500);
    }
}

function trackNewsClick(newsItem) {
    // Track news item clicks for analytics
    const title = newsItem.querySelector('.latest-news-title, .sub-news-title, .trending-title');
    const category = newsItem.querySelector('.news-category, .story-category');

    if (title && category) {
        console.log('News clicked:', {
            title: title.textContent.trim(),
            category: category.textContent.trim(),
            timestamp: new Date().toISOString()
        });

        // In production, send to analytics service
        // analytics.track('news_click', { ... });
    }
}

// Export functions for global use
window.trackAdClick = trackAdClick;
window.trackAdImpression = trackAdImpression;
window.shareArticle = shareArticle;
window.showNotification = showNotification;
window.initializeNewsHierarchy = initializeNewsHierarchy;
window.updateLatestNews = updateLatestNews;
window.checkBreakingNews = checkBreakingNews;
window.updateBreakingNewsBanner = updateBreakingNewsBanner;
window.showBreakingNewsBanner = showBreakingNewsBanner;

// Initialize breaking news system
document.addEventListener('DOMContentLoaded', function() {
    // Initial check for breaking news
    setTimeout(() => {
        checkBreakingNews();

        // If no breaking news found, show a welcome message
        setTimeout(() => {
            const banner = document.querySelector('.breaking-news-modern');
            if (banner && (banner.style.display === 'none' || !banner.querySelector('.breaking-item'))) {
                const sampleBreakingNews = [
                    {
                        title: "Welcome to NBC News Portal",
                        content: "Your trusted source for breaking news and latest updates from around the world."
                    }
                ];
                updateBreakingNewsBanner(sampleBreakingNews);
                showBreakingNewsBanner();
            }
        }, 2000);
    }, 1000);

    // Check for breaking news every 2 minutes
    setInterval(checkBreakingNews, 120000);
});
