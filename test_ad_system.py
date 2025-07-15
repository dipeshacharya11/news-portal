#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from news.models import Advertisement
from django.utils import timezone
from datetime import timedelta

def test_ad_system():
    """Test the ad system with active and inactive ads"""
    
    # First, deactivate all existing ads
    Advertisement.objects.all().update(is_active=False)
    print("✅ Deactivated all existing ads")
    
    # Create one active header ad
    active_ad, created = Advertisement.objects.get_or_create(
        title="ACTIVE Header Ad - Test",
        ad_type="header",
        defaults={
            'ad_size': '728x90',
            'html_content': '''
                <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); 
                           height: 90px; display: flex; align-items: center; justify-content: center; 
                           color: white; font-family: Arial, sans-serif; border-radius: 8px;">
                    <div class="text-center">
                        <h4 style="margin: 0; font-size: 18px;">✅ ACTIVE HEADER AD</h4>
                        <p style="margin: 5px 0 0 0; font-size: 12px;">This ad is active and should display</p>
                    </div>
                </div>
            ''',
            'url': 'https://example.com/active-ad',
            'is_active': True,
            'start_date': timezone.now(),
            'end_date': timezone.now() + timedelta(days=30),
        }
    )
    
    # Create inactive ads for different positions
    inactive_ads = [
        {
            'title': 'INACTIVE Banner Ad - Test',
            'ad_type': 'banner',
            'ad_size': '970x250',
            'is_active': False,
        },
        {
            'title': 'INACTIVE Sidebar Ad - Test',
            'ad_type': 'sidebar',
            'ad_size': '300x250',
            'is_active': False,
        },
        {
            'title': 'INACTIVE Footer Ad - Test',
            'ad_type': 'footer',
            'ad_size': '728x90',
            'is_active': False,
        }
    ]
    
    for ad_data in inactive_ads:
        ad, created = Advertisement.objects.get_or_create(
            title=ad_data['title'],
            ad_type=ad_data['ad_type'],
            defaults={
                'ad_size': ad_data['ad_size'],
                'html_content': f'''
                    <div style="background: #dc3545; height: 100px; display: flex; align-items: center; 
                               justify-content: center; color: white;">
                        <h4>❌ INACTIVE {ad_data['ad_type'].upper()} AD</h4>
                    </div>
                ''',
                'url': 'https://example.com/inactive-ad',
                'is_active': ad_data['is_active'],
                'start_date': timezone.now(),
                'end_date': timezone.now() + timedelta(days=30),
            }
        )
    
    # Show current status
    print("\n" + "="*50)
    print("AD SYSTEM TEST STATUS")
    print("="*50)
    
    all_ads = Advertisement.objects.all()
    active_ads = Advertisement.objects.filter(is_active=True)
    inactive_ads = Advertisement.objects.filter(is_active=False)
    
    print(f"Total ads: {all_ads.count()}")
    print(f"Active ads: {active_ads.count()}")
    print(f"Inactive ads: {inactive_ads.count()}")
    
    print("\nACTIVE ADS:")
    for ad in active_ads:
        print(f"  ✅ {ad.title} ({ad.ad_type} - {ad.ad_size})")
    
    print("\nINACTIVE ADS:")
    for ad in inactive_ads[:5]:  # Show first 5 inactive ads
        print(f"  ❌ {ad.title} ({ad.ad_type} - {ad.ad_size})")
    
    if inactive_ads.count() > 5:
        print(f"  ... and {inactive_ads.count() - 5} more inactive ads")
    
    print("\n" + "="*50)
    print("EXPECTED BEHAVIOR:")
    print("- Only the ACTIVE Header Ad should display")
    print("- All other ad positions should be hidden")
    print("- No placeholder/fallback ads should show")
    print("="*50)

if __name__ == "__main__":
    test_ad_system()
