#!/usr/bin/env python
import os
import sys
import django
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import shutil

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from news.models import News, Category, Author
from django.contrib.auth.models import User

def create_sample_news():
    # Create or get categories
    politics_cat, _ = Category.objects.get_or_create(name="Politics")
    tech_cat, _ = Category.objects.get_or_create(name="Technology") 
    sports_cat, _ = Category.objects.get_or_create(name="Sports")
    
    # Create or get author
    user, _ = User.objects.get_or_create(username="admin", defaults={
        'email': 'admin@example.com',
        'first_name': 'Admin',
        'last_name': 'User'
    })
    author, _ = Author.objects.get_or_create(user=user)
    
    # Sample news data with image URLs
    sample_news = [
        {
            'title': 'Breaking: Major Political Development Shakes Capitol',
            'description': 'In a stunning turn of events, new legislation has been proposed that could reshape the political landscape.',
            'content': 'This is the full content of the political news article...',
            'category': politics_cat,
            'thumbnail_url': 'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=800&h=600&fit=crop',
            'is_breaking': True,
            'is_featured': True,
            'is_trending': True,
        },
        {
            'title': 'Tech Giants Announce Revolutionary AI Breakthrough',
            'description': 'Leading technology companies have unveiled groundbreaking artificial intelligence capabilities.',
            'content': 'This is the full content of the technology news article...',
            'category': tech_cat,
            'thumbnail_url': 'https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=800&h=600&fit=crop',
            'is_featured': True,
            'is_trending': True,
        },
        {
            'title': 'Sports Championship Finals Draw Record Viewership',
            'description': 'The championship finals have broken all previous viewership records with millions tuning in.',
            'content': 'This is the full content of the sports news article...',
            'category': sports_cat,
            'thumbnail_url': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800&h=600&fit=crop',
            'is_trending': True,
        },
        {
            'title': 'Economic Markets Show Strong Recovery Signs',
            'description': 'Financial analysts report positive indicators as markets continue their upward trajectory.',
            'content': 'This is the full content of the economic news article...',
            'category': politics_cat,
            'thumbnail_url': 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800&h=600&fit=crop',
            'is_featured': True,
        },
        {
            'title': 'Climate Summit Reaches Historic Agreement',
            'description': 'World leaders have reached a consensus on new climate action initiatives.',
            'content': 'This is the full content of the climate news article...',
            'category': politics_cat,
            'thumbnail_url': 'https://images.unsplash.com/photo-1569163139394-de4e4f43e4e3?w=800&h=600&fit=crop',
            'is_trending': True,
        },
        {
            'title': 'Space Mission Achieves Milestone Discovery',
            'description': 'NASA announces significant findings from their latest space exploration mission.',
            'content': 'This is the full content of the space news article...',
            'category': tech_cat,
            'thumbnail_url': 'https://images.unsplash.com/photo-1446776653964-20c1d3a81b06?w=800&h=600&fit=crop',
            'is_featured': True,
        }
    ]
    
    # Create news items
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
        else:
            print(f"News already exists: {news.title}")

if __name__ == "__main__":
    create_sample_news()
    print("Sample news creation completed!")
