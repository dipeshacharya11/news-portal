// Enhanced UI JavaScript for News Portal

class NewsPortalUI {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeComponents();
        this.setupResponsiveBehavior();
        this.setupAccessibility();
        this.setupPerformanceOptimizations();
    }

    setupEventListeners() {
        // Navigation enhancements
        this.setupNavigation();
        
        // News card interactions
        this.setupNewsCards();
        
        // Breaking news ticker
        this.setupBreakingNews();
        
        // Advertisement management
        this.setupAdvertisements();
        
        // Search functionality
        this.setupSearch();
        
        // Category filtering
        this.setupCategoryFilter();
        
        // Lazy loading
        this.setupLazyLoading();
        
        // Scroll effects
        this.setupScrollEffects();
    }

    setupNavigation() {
        const navbar = document.querySelector('.navbar-modern');
        const navbarToggler = document.querySelector('.navbar-toggler');
        const navbarCollapse = document.querySelector('.navbar-collapse');

        // Sticky navigation
        window.addEventListener('scroll', () => {
            if (window.scrollY > 100) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });

        // Mobile menu toggle
        if (navbarToggler && navbarCollapse) {
            navbarToggler.addEventListener('click', (e) => {
                e.preventDefault();
                navbarCollapse.classList.toggle('show');
                
                // Update aria-expanded
                const isExpanded = navbarCollapse.classList.contains('show');
                navbarToggler.setAttribute('aria-expanded', isExpanded);
            });

            // Close mobile menu when clicking outside
            document.addEventListener('click', (e) => {
                if (!navbar.contains(e.target)) {
                    navbarCollapse.classList.remove('show');
                    navbarToggler.setAttribute('aria-expanded', 'false');
                }
            });
        }

        // Dropdown enhancements
        const dropdowns = document.querySelectorAll('.dropdown');
        dropdowns.forEach(dropdown => {
            const toggle = dropdown.querySelector('.dropdown-toggle');
            const menu = dropdown.querySelector('.dropdown-menu');

            if (toggle && menu) {
                // Keyboard navigation
                toggle.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        dropdown.classList.toggle('show');
                    }
                });

                // Close dropdown when clicking outside
                document.addEventListener('click', (e) => {
                    if (!dropdown.contains(e.target)) {
                        dropdown.classList.remove('show');
                    }
                });
            }
        });
    }

    setupNewsCards() {
        const newsCards = document.querySelectorAll('.news-card, .entity_wrapper');
        
        newsCards.forEach(card => {
            // Add hover effects
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-4px)';
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
            });

            // Add click tracking
            const link = card.querySelector('a');
            if (link) {
                link.addEventListener('click', (e) => {
                    this.trackNewsClick(link.href, card.dataset.newsId);
                });
            }

            // Add keyboard navigation
            card.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    const link = card.querySelector('a');
                    if (link) {
                        link.click();
                    }
                }
            });

            // Make cards focusable
            card.setAttribute('tabindex', '0');
            card.setAttribute('role', 'article');
        });
    }

    setupBreakingNews() {
        const breakingNews = document.querySelector('.breaking-news');
        if (!breakingNews) return;

        const breakingText = breakingNews.querySelector('.breaking-text');
        const breakingClose = breakingNews.querySelector('.breaking-close');

        // Auto-scroll breaking news text
        if (breakingText) {
            this.setupTextScroller(breakingText);
        }

        // Close breaking news
        if (breakingClose) {
            breakingClose.addEventListener('click', () => {
                breakingNews.style.display = 'none';
                localStorage.setItem('breakingNewsClosed', 'true');
            });
        }

        // Check if user previously closed breaking news
        if (localStorage.getItem('breakingNewsClosed') === 'true') {
            breakingNews.style.display = 'none';
        }
    }

    setupTextScroller(element) {
        const text = element.textContent;
        const container = element.parentElement;
        
        if (text.length > 100) {
            element.innerHTML = text + ' • ' + text;
            element.style.animation = 'scroll-left 20s linear infinite';
        }
    }

    setupAdvertisements() {
        const adSections = document.querySelectorAll('.ad-section, .horizontal-banner-ad, .bottom-banner-ad');
        
        adSections.forEach(section => {
            const adContent = section.querySelector('.ad-content');
            
            if (adContent) {
                // Add loading state
                adContent.classList.add('loading-skeleton');
                
                // Simulate ad loading
                setTimeout(() => {
                    adContent.classList.remove('loading-skeleton');
                }, 2000);

                // Track ad impressions
                this.trackAdImpression(section.dataset.adId);
            }
        });
    }

    setupSearch() {
        const searchForm = document.querySelector('.search-form');
        const searchInput = document.querySelector('.search-input');

        if (searchForm && searchInput) {
            // Auto-complete functionality
            searchInput.addEventListener('input', (e) => {
                const query = e.target.value;
                if (query.length > 2) {
                    this.showSearchSuggestions(query);
                } else {
                    this.hideSearchSuggestions();
                }
            });

            // Search form submission
            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const query = searchInput.value.trim();
                if (query) {
                    this.performSearch(query);
                }
            });
        }
    }

    setupCategoryFilter() {
        const categoryButtons = document.querySelectorAll('.category-filter-btn');
        const newsGrid = document.querySelector('.news-grid');

        categoryButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const category = button.dataset.category;
                
                // Update active button
                categoryButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');

                // Filter news
                this.filterNewsByCategory(category);
            });
        });
    }

    setupLazyLoading() {
        const images = document.querySelectorAll('img[loading="lazy"]');
        
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy-load');
                        img.classList.add('loaded');
                        observer.unobserve(img);
                    }
                });
            });

            images.forEach(img => {
                imageObserver.observe(img);
            });
        } else {
            // Fallback for older browsers
            images.forEach(img => {
                img.src = img.dataset.src;
            });
        }
    }

    setupScrollEffects() {
        // Parallax effect for hero images
        const heroImages = document.querySelectorAll('.hero-image');
        
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            
            heroImages.forEach(image => {
                const rate = scrolled * -0.5;
                image.style.transform = `translateY(${rate}px)`;
            });
        });

        // Fade in elements on scroll
        const fadeElements = document.querySelectorAll('.fade-in');
        
        if ('IntersectionObserver' in window) {
            const fadeObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('fade-in-visible');
                    }
                });
            });

            fadeElements.forEach(element => {
                fadeObserver.observe(element);
            });
        }
    }

    setupResponsiveBehavior() {
        // Handle viewport changes
        let resizeTimer;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                this.updateLayoutForViewport();
            }, 250);
        });

        // Initial layout update
        this.updateLayoutForViewport();
    }

    updateLayoutForViewport() {
        const viewport = window.innerWidth;
        const newsCards = document.querySelectorAll('.news-card');
        const statsGrid = document.querySelector('.stats-grid');

        // Adjust grid columns based on viewport
        if (statsGrid) {
            if (viewport < 640) {
                statsGrid.style.gridTemplateColumns = '1fr';
            } else if (viewport < 1024) {
                statsGrid.style.gridTemplateColumns = 'repeat(2, 1fr)';
            } else {
                statsGrid.style.gridTemplateColumns = 'repeat(4, 1fr)';
            }
        }

        // Adjust news card layout
        newsCards.forEach(card => {
            if (viewport < 768) {
                card.classList.add('mobile-layout');
            } else {
                card.classList.remove('mobile-layout');
            }
        });
    }

    setupAccessibility() {
        // Skip to main content link
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.textContent = 'Skip to main content';
        skipLink.className = 'skip-link';
        document.body.insertBefore(skipLink, document.body.firstChild);

        // Add ARIA labels
        const buttons = document.querySelectorAll('button:not([aria-label])');
        buttons.forEach(button => {
            if (!button.textContent.trim()) {
                button.setAttribute('aria-label', button.title || 'Button');
            }
        });

        // Focus management
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });

        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-navigation');
        });
    }

    setupPerformanceOptimizations() {
        // Debounce scroll events
        let scrollTimer;
        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimer);
            scrollTimer = setTimeout(() => {
                this.handleScrollOptimized();
            }, 16); // ~60fps
        });

        // Preload critical images
        this.preloadCriticalImages();

        // Service worker registration (if available)
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js')
                .then(registration => {
                    console.log('SW registered: ', registration);
                })
                .catch(registrationError => {
                    console.log('SW registration failed: ', registrationError);
                });
        }
    }

    // Utility methods
    trackNewsClick(url, newsId) {
        // Analytics tracking
        if (typeof gtag !== 'undefined') {
            gtag('event', 'news_click', {
                'news_id': newsId,
                'news_url': url
            });
        }
    }

    trackAdImpression(adId) {
        // Ad impression tracking
        if (typeof gtag !== 'undefined') {
            gtag('event', 'ad_impression', {
                'ad_id': adId
            });
        }
    }

    showSearchSuggestions(query) {
        // Implement search suggestions
        const suggestionsContainer = document.querySelector('.search-suggestions');
        if (suggestionsContainer) {
            // Fetch suggestions from API
            fetch(`/api/search/suggestions?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    this.renderSearchSuggestions(data.suggestions);
                })
                .catch(error => {
                    console.error('Error fetching suggestions:', error);
                });
        }
    }

    hideSearchSuggestions() {
        const suggestionsContainer = document.querySelector('.search-suggestions');
        if (suggestionsContainer) {
            suggestionsContainer.innerHTML = '';
            suggestionsContainer.style.display = 'none';
        }
    }

    renderSearchSuggestions(suggestions) {
        const container = document.querySelector('.search-suggestions');
        if (!container) return;

        container.innerHTML = '';
        container.style.display = 'block';

        suggestions.forEach(suggestion => {
            const item = document.createElement('div');
            item.className = 'suggestion-item';
            item.textContent = suggestion.title;
            item.addEventListener('click', () => {
                this.performSearch(suggestion.title);
            });
            container.appendChild(item);
        });
    }

    performSearch(query) {
        // Navigate to search results
        window.location.href = `/search/?q=${encodeURIComponent(query)}`;
    }

    filterNewsByCategory(category) {
        const newsItems = document.querySelectorAll('.news-card, .entity_wrapper');
        
        newsItems.forEach(item => {
            const itemCategory = item.dataset.category;
            if (category === 'all' || itemCategory === category) {
                item.style.display = 'block';
                item.classList.add('fade-in');
            } else {
                item.style.display = 'none';
            }
        });
    }

    preloadCriticalImages() {
        const criticalImages = [
            '/static/assets/img/feature-top.jpg',
            '/static/assets/img/category_img1.jpg',
            '/static/assets/img/category_img2.jpg'
        ];

        criticalImages.forEach(src => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'image';
            link.href = src;
            document.head.appendChild(link);
        });
    }

    handleScrollOptimized() {
        // Optimized scroll handling
        const scrolled = window.pageYOffset;
        const navbar = document.querySelector('.navbar-modern');
        
        if (navbar) {
            if (scrolled > 100) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }
    }

    initializeComponents() {
        // Initialize tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });

        // Initialize popovers
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(function (popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });

        // Initialize modals
        const modalTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="modal"]'));
        modalTriggerList.map(function (modalTriggerEl) {
            return new bootstrap.Modal(modalTriggerEl);
        });
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new NewsPortalUI();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NewsPortalUI;
} 