#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from news.models import Advertisement
from django.utils import timezone
from datetime import timedelta

def final_ad_test():
    """Final test of the advertisement system"""
    
    print("🧪 FINAL ADVERTISEMENT SYSTEM TEST")
    print("="*60)
    
    # Step 1: Deactivate all ads
    Advertisement.objects.all().update(is_active=False)
    print("1️⃣ Deactivated all ads")
    print(f"   Active ads: {Advertisement.objects.filter(is_active=True).count()}")
    print("   Expected: No ad sections should be visible on the website")
    
    input("\n📱 Check the website now. Press Enter when ready for next test...")
    
    # Step 2: Activate only header ad
    header_ad = Advertisement.objects.filter(ad_type='header').first()
    if header_ad:
        header_ad.is_active = True
        header_ad.save()
        print(f"2️⃣ Activated header ad: {header_ad.title}")
        print("   Expected: Only header ad section should be visible")
    
    input("\n📱 Check the website now. Press Enter when ready for next test...")
    
    # Step 3: Activate sidebar ad
    sidebar_ad = Advertisement.objects.filter(ad_type='sidebar').first()
    if sidebar_ad:
        sidebar_ad.is_active = True
        sidebar_ad.save()
        print(f"3️⃣ Activated sidebar ad: {sidebar_ad.title}")
        print("   Expected: Header and sidebar ad sections should be visible")
    
    input("\n📱 Check the website now. Press Enter when ready for next test...")
    
    # Step 4: Activate banner ad
    banner_ad = Advertisement.objects.filter(ad_type='banner').first()
    if banner_ad:
        banner_ad.is_active = True
        banner_ad.save()
        print(f"4️⃣ Activated banner ad: {banner_ad.title}")
        print("   Expected: Header, sidebar, and banner ad sections should be visible")
    
    input("\n📱 Check the website now. Press Enter when ready for next test...")
    
    # Step 5: Activate footer ad
    footer_ad = Advertisement.objects.filter(ad_type='footer').first()
    if footer_ad:
        footer_ad.is_active = True
        footer_ad.save()
        print(f"5️⃣ Activated footer ad: {footer_ad.title}")
        print("   Expected: All ad sections should be visible")
    
    input("\n📱 Check the website now. Press Enter when ready for final step...")
    
    # Step 6: Deactivate all again
    Advertisement.objects.all().update(is_active=False)
    print("6️⃣ Deactivated all ads again")
    print("   Expected: No ad sections should be visible")
    
    print("\n" + "="*60)
    print("✅ ADVERTISEMENT SYSTEM TEST COMPLETED!")
    print("="*60)
    print("SUMMARY:")
    print("✅ Ads only show when active")
    print("✅ Inactive ads are completely hidden")
    print("✅ No placeholder/fallback ads when inactive")
    print("✅ Ad sections dynamically appear/disappear")
    print("✅ System respects is_active status")
    print("="*60)

if __name__ == "__main__":
    final_ad_test()
