#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.utils import timezone
from datetime import timedelta
import random
from news.models import Advertisement, BreakingNews, Newsletter

def create_sample_ads():
    print("Clearing existing data...")
    Advertisement.objects.all().delete()
    BreakingNews.objects.all().delete()

    print("Creating sample advertisements...")
    
    # Sample advertisements
    ads_data = [
        {
            'title': 'NBC News Premium Subscription',
            'ad_type': 'banner',
            'ad_size': '728x90',
            'html_content': '''
            <div style="background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 20px; text-align: center; border-radius: 8px;">
                <h3 style="margin: 0; font-size: 24px;">Get NBC News Premium</h3>
                <p style="margin: 10px 0; font-size: 16px;">Ad-free experience, exclusive content, and breaking news alerts</p>
                <button style="background: white; color: #1e3a8a; border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold; cursor: pointer;">
                    Subscribe Now - $9.99/month
                </button>
            </div>
            ''',
            'url': 'https://www.nbcnews.com/premium',
        },
        {
            'title': 'Tech Conference 2024',
            'ad_type': 'sidebar',
            'ad_size': '300x250',
            'html_content': '''
            <div style="background: #f8f9fa; border: 2px solid #e9ecef; padding: 15px; text-align: center; border-radius: 8px;">
                <h4 style="color: #1e3a8a; margin-top: 0;">Tech Summit 2024</h4>
                <p style="font-size: 14px; color: #6c757d;">Join industry leaders for the biggest tech event of the year</p>
                <div style="background: #1e3a8a; color: white; padding: 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">
                    Early Bird: 50% OFF
                </div>
                <button style="background: #dc2626; color: white; border: none; padding: 8px 16px; border-radius: 4px; margin-top: 10px; cursor: pointer;">
                    Register Now
                </button>
            </div>
            ''',
            'url': 'https://techsummit2024.com',
        },
        {
            'title': 'Mobile App Download',
            'ad_type': 'popup',
            'ad_size': '300x250',
            'html_content': '''
            <div style="background: white; padding: 20px; text-align: center; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
                <h3 style="color: #1e3a8a; margin-top: 0;">Download NBC News App</h3>
                <p style="color: #6c757d; font-size: 14px;">Get breaking news alerts and stay informed on the go</p>
                <div style="margin: 15px 0;">
                    <span style="background: #1e3a8a; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px;">⭐ 4.8 Rating</span>
                </div>
                <button style="background: #1e3a8a; color: white; border: none; padding: 12px 24px; border-radius: 6px; font-weight: bold; cursor: pointer; width: 100%;">
                    Download Free
                </button>
            </div>
            ''',
            'url': 'https://apps.apple.com/nbcnews',
        }
    ]

    # Create advertisements
    for ad_data in ads_data:
        start_date = timezone.now() - timedelta(days=random.randint(1, 10))
        end_date = timezone.now() + timedelta(days=random.randint(30, 90))
        
        ad, created = Advertisement.objects.get_or_create(
            title=ad_data['title'],
            defaults={
                'ad_type': ad_data['ad_type'],
                'ad_size': ad_data['ad_size'],
                'html_content': ad_data['html_content'],
                'url': ad_data['url'],
                'is_active': True,
                'start_date': start_date,
                'end_date': end_date,
                'clicks': random.randint(10, 500),
                'impressions': random.randint(1000, 10000)
            }
        )
        
        if created:
            print(f'Created advertisement: {ad.title}')
        else:
            print(f'Advertisement already exists: {ad.title}')

    # Create breaking news
    breaking_news_data = [
        {
            'title': 'LIVE: Major Economic Summit in Progress',
            'content': 'World leaders are currently meeting to discuss global economic policies and climate change initiatives.',
        },
        {
            'title': 'URGENT: Weather Alert Issued for Multiple States',
            'content': 'Severe weather conditions expected across the region. Residents advised to take necessary precautions.',
        }
    ]

    for news_data in breaking_news_data:
        breaking_news, created = BreakingNews.objects.get_or_create(
            title=news_data['title'],
            defaults={
                'content': news_data['content'],
                'is_active': True,
                'expires_at': timezone.now() + timedelta(hours=24)
            }
        )
        if created:
            print(f'Created breaking news: {breaking_news.title}')
        else:
            print(f'Breaking news already exists: {breaking_news.title}')

    print("Sample data creation completed!")

if __name__ == '__main__':
    create_sample_ads()
