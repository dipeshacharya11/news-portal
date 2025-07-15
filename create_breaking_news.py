#!/usr/bin/env python
import os
import sys
import django
from datetime import timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from news.models import News, Category, Author, BreakingNews
from django.contrib.auth.models import User
from django.utils import timezone

def create_breaking_news():
    print("Creating fresh breaking news...")
    
    # Clear old breaking news
    BreakingNews.objects.all().delete()
    
    # Create fresh breaking news
    breaking_news_data = [
        {
            'title': 'LIVE: Major Technology Conference Underway',
            'content': 'Tech leaders from around the world are announcing groundbreaking innovations in AI and quantum computing.',
        },
        {
            'title': 'URGENT: Global Climate Summit Reaches Historic Agreement',
            'content': 'World leaders have reached a consensus on new climate action initiatives with immediate implementation.',
        },
        {
            'title': 'BREAKING: Economic Markets Show Record Growth',
            'content': 'Stock markets worldwide are experiencing unprecedented growth following new trade agreements.',
        }
    ]
    
    for news_data in breaking_news_data:
        breaking_news = BreakingNews.objects.create(
            title=news_data['title'],
            content=news_data['content'],
            is_active=True,
            expires_at=timezone.now() + timedelta(hours=48)  # Valid for 48 hours
        )
        print(f'Created breaking news: {breaking_news.title}')
    
    # Also mark some regular news as breaking
    try:
        # Get some existing news and mark them as breaking
        regular_news = News.objects.filter(is_published=True, is_breaking=False)[:3]
        for news in regular_news:
            news.is_breaking = True
            news.priority = 'breaking'
            news.save()
            print(f'Marked as breaking: {news.title}')
    except Exception as e:
        print(f'Error updating regular news: {e}')
    
    print("Breaking news creation completed!")
    print(f"Total breaking news alerts: {BreakingNews.objects.filter(is_active=True).count()}")
    print(f"Total breaking news items: {News.objects.filter(is_breaking=True, is_published=True).count()}")

if __name__ == "__main__":
    create_breaking_news()
