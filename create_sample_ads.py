#!/usr/bin/env python
import os
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from news.models import Advertisement
from django.utils import timezone

def create_sample_ads():
    """Create sample advertisements for testing"""
    
    # Sample ad data
    sample_ads = [
        {
            'title': 'Premium Tech Solutions',
            'ad_type': 'header',
            'ad_size': '728x90',
            'html_content': '''
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                           height: 90px; display: flex; align-items: center; justify-content: center; 
                           color: white; font-family: Arial, sans-serif; border-radius: 8px;">
                    <div class="text-center">
                        <h4 style="margin: 0; font-size: 18px;">🚀 Premium Tech Solutions</h4>
                        <p style="margin: 5px 0 0 0; font-size: 12px;">Advanced technology for modern businesses</p>
                    </div>
                </div>
            ''',
            'url': 'https://example.com/tech-solutions',
            'is_active': True,
        },
        {
            'title': 'Digital Marketing Agency',
            'ad_type': 'banner',
            'ad_size': '970x250',
            'html_content': '''
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                           height: 250px; display: flex; align-items: center; justify-content: center; 
                           color: white; font-family: Arial, sans-serif; border-radius: 12px; 
                           box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                    <div class="text-center">
                        <h2 style="margin: 0; font-size: 32px; font-weight: bold;">📈 Digital Marketing</h2>
                        <p style="margin: 10px 0; font-size: 18px;">Grow your business with our expert marketing strategies</p>
                        <div style="background: rgba(255,255,255,0.2); padding: 8px 20px; border-radius: 25px; 
                                   display: inline-block; margin-top: 10px; font-size: 14px;">
                            Click to learn more →
                        </div>
                    </div>
                </div>
            ''',
            'url': 'https://example.com/digital-marketing',
            'is_active': True,
        },
        {
            'title': 'E-commerce Platform',
            'ad_type': 'sidebar',
            'ad_size': '300x250',
            'html_content': '''
                <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                           height: 250px; display: flex; align-items: center; justify-content: center; 
                           color: white; font-family: Arial, sans-serif; border-radius: 10px; 
                           text-align: center; padding: 20px; box-sizing: border-box;">
                    <div>
                        <h3 style="margin: 0 0 15px 0; font-size: 22px;">🛒 E-commerce</h3>
                        <p style="margin: 0 0 15px 0; font-size: 14px; line-height: 1.4;">
                            Build your online store with our powerful platform
                        </p>
                        <div style="background: rgba(255,255,255,0.2); padding: 6px 15px; border-radius: 20px; 
                                   font-size: 12px; display: inline-block;">
                            Start Free Trial
                        </div>
                    </div>
                </div>
            ''',
            'url': 'https://example.com/ecommerce',
            'is_active': True,
        },
        {
            'title': 'Cloud Services',
            'ad_type': 'sidebar',
            'ad_size': '300x250',
            'html_content': '''
                <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
                           height: 250px; display: flex; align-items: center; justify-content: center; 
                           color: #333; font-family: Arial, sans-serif; border-radius: 10px; 
                           text-align: center; padding: 20px; box-sizing: border-box;">
                    <div>
                        <h3 style="margin: 0 0 15px 0; font-size: 22px;">☁️ Cloud Services</h3>
                        <p style="margin: 0 0 15px 0; font-size: 14px; line-height: 1.4;">
                            Secure, scalable cloud solutions for your business
                        </p>
                        <div style="background: rgba(0,0,0,0.1); padding: 6px 15px; border-radius: 20px; 
                                   font-size: 12px; display: inline-block;">
                            Learn More
                        </div>
                    </div>
                </div>
            ''',
            'url': 'https://example.com/cloud-services',
            'is_active': True,
        },
        {
            'title': 'Financial Services',
            'ad_type': 'footer',
            'ad_size': '728x90',
            'html_content': '''
                <div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
                           height: 90px; display: flex; align-items: center; justify-content: center; 
                           color: #333; font-family: Arial, sans-serif; border-radius: 8px;">
                    <div class="text-center">
                        <h4 style="margin: 0; font-size: 18px;">💰 Financial Services</h4>
                        <p style="margin: 5px 0 0 0; font-size: 12px;">Smart investment solutions for your future</p>
                    </div>
                </div>
            ''',
            'url': 'https://example.com/financial-services',
            'is_active': True,
        },
        {
            'title': 'Educational Platform',
            'ad_type': 'sidebar',
            'ad_size': '300x250',
            'html_content': '''
                <div style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); 
                           height: 250px; display: flex; align-items: center; justify-content: center; 
                           color: #333; font-family: Arial, sans-serif; border-radius: 10px; 
                           text-align: center; padding: 20px; box-sizing: border-box;">
                    <div>
                        <h3 style="margin: 0 0 15px 0; font-size: 22px;">📚 Learn Online</h3>
                        <p style="margin: 0 0 15px 0; font-size: 14px; line-height: 1.4;">
                            Master new skills with our comprehensive courses
                        </p>
                        <div style="background: rgba(0,0,0,0.1); padding: 6px 15px; border-radius: 20px; 
                                   font-size: 12px; display: inline-block;">
                            Start Learning
                        </div>
                    </div>
                </div>
            ''',
            'url': 'https://example.com/education',
            'is_active': True,
        }
    ]
    
    # Create advertisements
    created_count = 0
    for ad_data in sample_ads:
        ad, created = Advertisement.objects.get_or_create(
            title=ad_data['title'],
            ad_type=ad_data['ad_type'],
            defaults={
                'ad_size': ad_data['ad_size'],
                'html_content': ad_data['html_content'],
                'url': ad_data['url'],
                'is_active': ad_data['is_active'],
                'start_date': timezone.now(),
                'end_date': timezone.now() + timedelta(days=30),  # Active for 30 days
            }
        )
        
        if created:
            created_count += 1
            print(f"Created ad: {ad.title} ({ad.ad_type} - {ad.ad_size})")
        else:
            print(f"Ad already exists: {ad.title}")
    
    print(f"\nSample ads creation completed!")
    print(f"Created {created_count} new advertisements")
    print(f"Total active ads: {Advertisement.objects.filter(is_active=True).count()}")

if __name__ == "__main__":
    create_sample_ads()
