#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from news.models import Advertisement

def manage_ads():
    """Manage advertisement status"""
    
    print("Current Advertisement Status:")
    print("=" * 50)
    
    ads = Advertisement.objects.all()
    for ad in ads:
        status = "ACTIVE" if ad.is_active else "INACTIVE"
        print(f"ID: {ad.id} | {ad.title} | {ad.ad_type} | {status}")
    
    print(f"\nTotal ads: {ads.count()}")
    print(f"Active ads: {Advertisement.objects.filter(is_active=True).count()}")
    print(f"Inactive ads: {Advertisement.objects.filter(is_active=False).count()}")
    
    print("\nOptions:")
    print("1. Deactivate all ads")
    print("2. Activate all ads")
    print("3. Activate specific ads")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        # Deactivate all ads
        Advertisement.objects.all().update(is_active=False)
        print("✅ All ads have been deactivated!")
        
    elif choice == "2":
        # Activate all ads
        Advertisement.objects.all().update(is_active=True)
        print("✅ All ads have been activated!")
        
    elif choice == "3":
        # Activate specific ads
        print("\nSelect ads to activate (enter IDs separated by commas):")
        ad_ids = input("Ad IDs: ").strip()
        if ad_ids:
            try:
                ids = [int(id.strip()) for id in ad_ids.split(',')]
                Advertisement.objects.filter(id__in=ids).update(is_active=True)
                Advertisement.objects.exclude(id__in=ids).update(is_active=False)
                print(f"✅ Activated ads with IDs: {ids}")
            except ValueError:
                print("❌ Invalid input. Please enter valid ad IDs.")
        
    elif choice == "4":
        print("Exiting...")
        return
    
    else:
        print("❌ Invalid choice!")
    
    # Show updated status
    print("\nUpdated Status:")
    print("=" * 30)
    active_ads = Advertisement.objects.filter(is_active=True)
    if active_ads.exists():
        for ad in active_ads:
            print(f"✅ ACTIVE: {ad.title} ({ad.ad_type})")
    else:
        print("❌ No active ads")

if __name__ == "__main__":
    manage_ads()
