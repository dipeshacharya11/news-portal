#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from news.models import News, Category, Author
from mainsite.models import HomePageSettings
from django.contrib.auth.models import User

def quick_setup():
    # Create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True
        }
    )
    admin_user.set_password('admin123')
    admin_user.save()
    
    # Create author
    author, _ = Author.objects.get_or_create(user=admin_user)
    
    # Create categories
    categories = ['Politics', 'Technology', 'Sports', 'Business', 'World News']
    cat_objects = []
    for cat_name in categories:
        cat, _ = Category.objects.get_or_create(name=cat_name)
        cat_objects.append(cat)
    
    # Create sample news
    sample_news_data = [
        {
            'title': 'Breaking: Major Political Development in Washington',
            'description': 'Significant political changes are underway as new policies are being discussed in Congress.',
            'category': cat_objects[0],  # Politics
            'is_breaking': True,
            'is_featured': True,
            'is_trending': True,
        },
        {
            'title': 'Revolutionary AI Technology Unveiled by Tech Giants',
            'description': 'Leading technology companies showcase groundbreaking artificial intelligence capabilities.',
            'category': cat_objects[1],  # Technology
            'is_featured': True,
            'is_trending': True,
        },
        {
            'title': 'Championship Finals Break Viewership Records',
            'description': 'Sports fans worldwide tune in for the most-watched championship in history.',
            'category': cat_objects[2],  # Sports
            'is_trending': True,
        },
        {
            'title': 'Global Markets Show Strong Recovery',
            'description': 'Economic indicators point to sustained growth across major markets.',
            'category': cat_objects[3],  # Business
            'is_featured': True,
        },
        {
            'title': 'International Climate Summit Reaches Agreement',
            'description': 'World leaders unite on comprehensive climate action plan.',
            'category': cat_objects[4],  # World News
            'is_trending': True,
        },
        {
            'title': 'Space Exploration Mission Achieves Historic Milestone',
            'description': 'NASA announces successful completion of ambitious space mission.',
            'category': cat_objects[1],  # Technology
            'is_featured': True,
        },
        {
            'title': 'Healthcare Innovation Promises Better Treatment',
            'description': 'Medical breakthrough offers new hope for patients worldwide.',
            'category': cat_objects[1],  # Technology
            'is_trending': True,
        },
        {
            'title': 'Education Reform Initiative Gains Support',
            'description': 'New educational policies receive backing from educators and parents.',
            'category': cat_objects[0],  # Politics
            'is_featured': True,
        }
    ]
    
    # Create news items
    news_items = []
    for i, news_data in enumerate(sample_news_data):
        news, created = News.objects.get_or_create(
            title=news_data['title'],
            defaults={
                'author': author,
                'description': news_data['description'],
                'content': f"This is the full content for {news_data['title']}. " * 10,
                'category': news_data['category'],
                'is_published': True,
                'is_breaking': news_data.get('is_breaking', False),
                'is_featured': news_data.get('is_featured', False),
                'is_trending': news_data.get('is_trending', False),
            }
        )
        news_items.append(news)
        if created:
            print(f"Created: {news.title}")
    
    # Setup homepage settings
    homepage_settings, created = HomePageSettings.objects.get_or_create(
        id=1,
        defaults={
            'hot_news': news_items[0] if news_items else None,
            'trending': news_items[1] if len(news_items) > 1 else None,
            'editor_choice': news_items[2] if len(news_items) > 2 else None,
            'post_catalog_one': cat_objects[0],  # Politics
            'post_catalog_two': cat_objects[1],  # Technology
            'post_catalog_three': cat_objects[2],  # Sports
            'post_catalog_four': cat_objects[3],  # Business
            'post_catalog_five': cat_objects[4],  # World News
        }
    )
    
    if not created:
        homepage_settings.hot_news = news_items[0] if news_items else homepage_settings.hot_news
        homepage_settings.trending = news_items[1] if len(news_items) > 1 else homepage_settings.trending
        homepage_settings.editor_choice = news_items[2] if len(news_items) > 2 else homepage_settings.editor_choice
        homepage_settings.save()
    
    print(f"Setup complete!")
    print(f"Admin login: admin / admin123")
    print(f"Created {len(news_items)} news items")
    print(f"Created {len(cat_objects)} categories")

if __name__ == "__main__":
    quick_setup()
