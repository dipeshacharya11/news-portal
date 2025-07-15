#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from news.models import News, Category, Author
from mainsite.models import HomePageSettings
from django.contrib.auth.models import User

def add_news_with_images():
    """Add news items with external image URLs for testing"""
    
    # Get or create author
    admin_user = User.objects.get(username='admin')
    author = Author.objects.get(user=admin_user)
    
    # Get categories
    politics_cat = Category.objects.get(name="Politics")
    tech_cat = Category.objects.get(name="Technology")
    sports_cat = Category.objects.get(name="Sports")
    business_cat = Category.objects.get(name="Business")
    
    # News with external image URLs
    news_with_images = [
        {
            'title': 'Breaking: Major Political Development with Image',
            'description': 'This news item has an external image URL to test image display functionality.',
            'content': 'Full content of the political news with image testing...',
            'category': politics_cat,
            'thumbnail_url': 'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=800&h=600&fit=crop&crop=center',
            'is_breaking': True,
            'is_featured': True,
            'is_trending': True,
        },
        {
            'title': 'Tech Innovation with High-Quality Image',
            'description': 'Technology news featuring a beautiful external image to showcase proper image loading.',
            'content': 'Full content of the technology news with image testing...',
            'category': tech_cat,
            'thumbnail_url': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=600&fit=crop&crop=center',
            'is_featured': True,
            'is_trending': True,
        },
        {
            'title': 'Sports Championship with Action Photo',
            'description': 'Sports news with an exciting action photo to test image display in different contexts.',
            'content': 'Full content of the sports news with image testing...',
            'category': sports_cat,
            'thumbnail_url': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800&h=600&fit=crop&crop=center',
            'is_trending': True,
        },
        {
            'title': 'Business Growth with Professional Image',
            'description': 'Business news featuring a professional image to test corporate content display.',
            'content': 'Full content of the business news with image testing...',
            'category': business_cat,
            'thumbnail_url': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=600&fit=crop&crop=center',
            'is_featured': True,
        },
        {
            'title': 'Environmental News with Nature Photography',
            'description': 'Environmental story with stunning nature photography to test image quality.',
            'content': 'Full content of the environmental news with image testing...',
            'category': politics_cat,
            'thumbnail_url': 'https://images.unsplash.com/photo-1569163139394-de4e4f43e4e3?w=800&h=600&fit=crop&crop=center',
            'is_trending': True,
        },
        {
            'title': 'Space Exploration with Cosmic Images',
            'description': 'Space news featuring breathtaking cosmic imagery to test high-resolution display.',
            'content': 'Full content of the space news with image testing...',
            'category': tech_cat,
            'thumbnail_url': 'https://images.unsplash.com/photo-1446776653964-20c1d3a81b06?w=800&h=600&fit=crop&crop=center',
            'is_featured': True,
        }
    ]
    
    # Create news items
    created_count = 0
    for news_data in news_with_images:
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
            created_count += 1
            print(f"Created: {news.title}")
        else:
            print(f"Already exists: {news.title}")
    
    # Update homepage settings with image news
    homepage_settings = HomePageSettings.objects.first()
    if homepage_settings:
        # Set the first news with image as hot news
        image_news = News.objects.filter(thumbnail_url__isnull=False).exclude(thumbnail_url='').first()
        if image_news:
            homepage_settings.hot_news = image_news
            homepage_settings.save()
            print(f"Updated hot news to: {image_news.title}")
    
    print(f"\nNews with images creation completed!")
    print(f"Created {created_count} new news items with images")
    print(f"Total news with images: {News.objects.filter(thumbnail_url__isnull=False).exclude(thumbnail_url='').count()}")

if __name__ == "__main__":
    add_news_with_images()
