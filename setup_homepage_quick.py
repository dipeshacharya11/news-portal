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
    print("Setting up homepage...")
    
    # Create basic categories if they don't exist
    categories_data = [
        "Politics", "Technology", "Sports", "Business", "World News"
    ]
    
    categories = []
    for cat_name in categories_data:
        category, created = Category.objects.get_or_create(name=cat_name)
        categories.append(category)
        if created:
            print(f"Created category: {cat_name}")
    
    # Create a default user and author if they don't exist
    user, created = User.objects.get_or_create(
        username="admin",
        defaults={
            'email': 'admin@example.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    if created:
        user.set_password('admin123')
        user.save()
        print("Created admin user")
    
    author, created = Author.objects.get_or_create(user=user)
    if created:
        print("Created author")
    
    # Create some sample news if none exist
    if News.objects.count() == 0:
        sample_news = [
            {
                'title': 'Breaking: Major Political Development',
                'description': 'Important political news that affects everyone.',
                'content': 'This is a detailed article about the political development...',
                'category': categories[0],  # Politics
                'is_breaking': True,
                'is_featured': True
            },
            {
                'title': 'Tech Innovation Breakthrough',
                'description': 'New technology changes the industry.',
                'content': 'This article discusses the latest technology breakthrough...',
                'category': categories[1],  # Technology
                'is_trending': True
            },
            {
                'title': 'Sports Championship Results',
                'description': 'Latest results from the championship.',
                'content': 'Coverage of the recent sports championship...',
                'category': categories[2],  # Sports
            },
            {
                'title': 'Business Market Update',
                'description': 'Current market trends and analysis.',
                'content': 'Analysis of current business market conditions...',
                'category': categories[3],  # Business
            },
            {
                'title': 'World News Update',
                'description': 'International news and developments.',
                'content': 'Coverage of international events and news...',
                'category': categories[4],  # World News
            }
        ]
        
        created_news = []
        for news_data in sample_news:
            news = News.objects.create(
                author=author,
                title=news_data['title'],
                description=news_data['description'],
                content=news_data['content'],
                category=news_data['category'],
                is_published=True,
                is_breaking=news_data.get('is_breaking', False),
                is_featured=news_data.get('is_featured', False),
                is_trending=news_data.get('is_trending', False)
            )
            created_news.append(news)
            print(f"Created news: {news.title}")
    else:
        created_news = list(News.objects.all()[:5])
    
    # Create or update homepage settings
    homepage_settings, created = HomePageSettings.objects.get_or_create(
        id=1,
        defaults={
            'hot_news': created_news[0] if created_news else None,
            'trending': created_news[1] if len(created_news) > 1 else None,
            'editor_choice': created_news[2] if len(created_news) > 2 else None,
            'post_catalog_one': categories[0],
            'post_catalog_two': categories[1],
            'post_catalog_three': categories[2],
            'post_catalog_four': categories[3],
            'post_catalog_five': categories[4],
        }
    )
    
    if created:
        print("Created homepage settings")
    else:
        # Update existing settings
        if created_news:
            homepage_settings.hot_news = created_news[0]
            homepage_settings.trending = created_news[1] if len(created_news) > 1 else homepage_settings.trending
            homepage_settings.editor_choice = created_news[2] if len(created_news) > 2 else homepage_settings.editor_choice
        
        homepage_settings.post_catalog_one = categories[0]
        homepage_settings.post_catalog_two = categories[1]
        homepage_settings.post_catalog_three = categories[2]
        homepage_settings.post_catalog_four = categories[3]
        homepage_settings.post_catalog_five = categories[4]
        homepage_settings.save()
        print("Updated homepage settings")
    
    print("Homepage setup completed!")
    print(f"Categories: {len(categories)}")
    print(f"News items: {News.objects.count()}")
    print(f"Homepage settings: {'Created' if created else 'Updated'}")

if __name__ == "__main__":
    setup_homepage()
