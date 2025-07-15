#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from news.models import Advertisement

def activate_test_ads():
    """Activate a few test ads to verify the system works"""
    
    # Activate one ad of each type for testing
    ad_types_to_activate = ['header', 'banner', 'sidebar', 'footer']
    
    for ad_type in ad_types_to_activate:
        # Find the first inactive ad of this type and activate it
        ad = Advertisement.objects.filter(ad_type=ad_type, is_active=False).first()
        if ad:
            ad.is_active = True
            ad.save()
            print(f"✅ Activated: {ad.title} ({ad.ad_type})")
        else:
            print(f"❌ No inactive {ad_type} ads found")
    
    # Show current status
    print("\n" + "="*50)
    print("CURRENT ACTIVE ADS:")
    print("="*50)
    
    active_ads = Advertisement.objects.filter(is_active=True)
    for ad in active_ads:
        print(f"✅ {ad.title} ({ad.ad_type} - {ad.ad_size})")
    
    print(f"\nTotal active ads: {active_ads.count()}")
    print("Expected: All ad sections should now be visible")

if __name__ == "__main__":
    activate_test_ads()
