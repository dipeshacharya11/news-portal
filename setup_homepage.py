#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from news.models import News, Category, Author
from mainsite.models import HomePageSettings
from django.contrib.auth.models import User

def setup_homepage():
    # Create or get categories
    politics_cat, _ = Category.objects.get_or_create(name="Politics")
    tech_cat, _ = Category.objects.get_or_create(name="Technology") 
    sports_cat, _ = Category.objects.get_or_create(name="Sports")
    business_cat, _ = Category.objects.get_or_create(name="Business")
    world_cat, _ = Category.objects.get_or_create(name="World News")
    
    # Create or get author
    user, _ = User.objects.get_or_create(username="admin", defaults={
        'email': 'admin@example.com',
        'first_name': 'Admin',
        'last_name': 'User',
        'is_staff': True,
        'is_superuser': True
    })
    if user and not user.check_password('admin123'):
        user.set_password('admin123')
        user.save()
    
    author, _ = Author.objects.get_or_create(user=user)
    
    # Sample news data
    sample_news = [
        {
            'title': 'Breaking: Major Political Development Shakes Capitol',
            'description': 'In a stunning turn of events, new legislation has been proposed that could reshape the political landscape for years to come.',
            'content': 'This is the full content of the political news article with detailed information about the political developments...',
            'category': politics_cat,
            'thumbnail_url': 'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=800&h=600&fit=crop',
            'is_breaking': True,
            'is_featured': True,
            'is_trending': True,
        },
        {
            'title': 'Tech Giants Announce Revolutionary AI Breakthrough',
            'description': 'Leading technology companies have unveiled groundbreaking artificial intelligence capabilities that promise to transform industries.',
            'content': 'This is the full content of the technology news article...',
            'category': tech_cat,
            'thumbnail_url': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=600&fit=crop',
            'is_featured': True,
            'is_trending': True,
        },
        {
            'title': 'Sports Championship Finals Draw Record Viewership',
            'description': 'The championship finals have broken all previous viewership records with millions of fans tuning in worldwide.',
            'content': 'This is the full content of the sports news article...',
            'category': sports_cat,
            'thumbnail_url': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800&h=600&fit=crop',
            'is_trending': True,
        },
        {
            'title': 'Economic Markets Show Strong Recovery Signs',
            'description': 'Financial analysts report positive indicators as global markets continue their upward trajectory following recent policy changes.',
            'content': 'This is the full content of the economic news article...',
            'category': business_cat,
            'thumbnail_url': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=600&fit=crop',
            'is_featured': True,
        },
        {
            'title': 'Climate Summit Reaches Historic Agreement',
            'description': 'World leaders have reached a consensus on new climate action initiatives that could significantly impact global environmental policy.',
            'content': 'This is the full content of the climate news article...',
            'category': world_cat,
            'thumbnail_url': 'https://images.unsplash.com/photo-1569163139394-de4e4f43e4e3?w=800&h=600&fit=crop',
            'is_trending': True,
        },
        {
            'title': 'Space Mission Achieves Milestone Discovery',
            'description': 'NASA announces significant findings from their latest space exploration mission that could change our understanding of the universe.',
            'content': 'This is the full content of the space news article...',
            'category': tech_cat,
            'thumbnail_url': 'https://images.unsplash.com/photo-1446776653964-20c1d3a81b06?w=800&h=600&fit=crop',
            'is_featured': True,
        },
        {
            'title': 'Global Trade Relations Show Improvement',
            'description': 'International trade partnerships are strengthening as new agreements are reached between major economic powers.',
            'content': 'This is the full content of the trade news article...',
            'category': business_cat,
            'thumbnail_url': 'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800&h=600&fit=crop',
            'is_trending': True,
        },
        {
            'title': 'Healthcare Innovation Promises Better Treatment',
            'description': 'Medical researchers have developed new treatment methods that could revolutionize patient care worldwide.',
            'content': 'This is the full content of the healthcare news article...',
            'category': tech_cat,
            'thumbnail_url': 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&h=600&fit=crop',
            'is_featured': True,
        }
    ]
    
    # Create news items
    created_news = []
    for news_data in sample_news:
        news, created = News.objects.get_or_create(
            title=news_data['title'],
            defaults={
                'author': author,
                'description': news_data['description'],
                'content': news_data['content'],
                'category': news_data['category'],
                'thumbnail_url': news_data['thumbnail_url'],
                'is_published': True,
                'is_breaking': news_data.get('is_breaking', False),
                'is_featured': news_data.get('is_featured', False),
                'is_trending': news_data.get('is_trending', False),
            }
        )
        if created:
            print(f"Created news: {news.title}")
        created_news.append(news)
    
    # Setup homepage settings
    homepage_settings, created = HomePageSettings.objects.get_or_create(
        id=1,
        defaults={
            'hot_news': created_news[0] if created_news else None,
            'trending': created_news[1] if len(created_news) > 1 else None,
            'editor_choice': created_news[2] if len(created_news) > 2 else None,
            'post_catalog_one': politics_cat,
            'post_catalog_two': tech_cat,
            'post_catalog_three': sports_cat,
            'post_catalog_four': business_cat,
            'post_catalog_five': world_cat,
        }
    )
    
    if created:
        print("Created homepage settings")
    else:
        # Update existing settings
        homepage_settings.hot_news = created_news[0] if created_news else homepage_settings.hot_news
        homepage_settings.trending = created_news[1] if len(created_news) > 1 else homepage_settings.trending
        homepage_settings.editor_choice = created_news[2] if len(created_news) > 2 else homepage_settings.editor_choice
        homepage_settings.save()
        print("Updated homepage settings")

if __name__ == "__main__":
    setup_homepage()
    print("Homepage setup completed!")
