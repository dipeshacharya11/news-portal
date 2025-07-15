#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from news.models import News
from mainsite.models import HomePageSettings

def fix_images():
    print("Checking image issues...")
    
    # Check total news count
    total_news = News.objects.count()
    print(f"Total news items: {total_news}")
    
    # Check published news
    published_news = News.objects.filter(is_published=True).count()
    print(f"Published news items: {published_news}")
    
    # Check news with images
    news_with_thumbnail = News.objects.filter(thumbnail__isnull=False).count()
    news_with_thumbnail_url = News.objects.filter(thumbnail_url__isnull=False).exclude(thumbnail_url='').count()
    
    print(f"News with uploaded thumbnails: {news_with_thumbnail}")
    print(f"News with thumbnail URLs: {news_with_thumbnail_url}")
    
    # Check homepage settings
    try:
        homepage_settings = HomePageSettings.objects.first()
        if homepage_settings:
            print(f"Hot news: {homepage_settings.hot_news.title if homepage_settings.hot_news else 'None'}")
            print(f"Trending: {homepage_settings.trending.title if homepage_settings.trending else 'None'}")
            print(f"Editor choice: {homepage_settings.editor_choice.title if homepage_settings.editor_choice else 'None'}")
        else:
            print("No homepage settings found")
    except Exception as e:
        print(f"Error checking homepage settings: {e}")
    
    # Show first few news items
    print("\nFirst 3 news items:")
    for news in News.objects.filter(is_published=True)[:3]:
        print(f"- {news.title}")
        print(f"  Thumbnail: {news.thumbnail}")
        print(f"  Thumbnail URL: {news.thumbnail_url}")
        print(f"  Category: {news.category}")
        print()

if __name__ == "__main__":
    fix_images()
