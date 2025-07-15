#!/usr/bin/env python
"""
Error checking script for the News Portal
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

try:
    # Initialize Django
    django.setup()
    print("✅ Django setup successful")
    
    # Test model imports
    try:
        from news.models import News, Category, Advertisement, BreakingNews, Newsletter
        print("✅ News models imported successfully")
    except ImportError as e:
        print(f"❌ Error importing news models: {e}")
    
    # Test admin imports
    try:
        from news.admin import NewsAdmin, CategoryAdmin
        print("✅ Admin classes imported successfully")
    except ImportError as e:
        print(f"❌ Error importing admin classes: {e}")
    
    # Test custom admin imports
    try:
        from custom_admin.views import DashboardView
        print("✅ Custom admin views imported successfully")
    except ImportError as e:
        print(f"❌ Error importing custom admin views: {e}")
    
    # Test API views
    try:
        from news.api.ad_views import get_banner_ad
        print("✅ API views imported successfully")
    except ImportError as e:
        print(f"❌ Error importing API views: {e}")
    
    # Test URL patterns
    try:
        from django.urls import reverse
        from django.test import RequestFactory
        
        # Test some basic URL patterns
        factory = RequestFactory()
        request = factory.get('/')
        
        print("✅ URL patterns test passed")
    except Exception as e:
        print(f"❌ Error with URL patterns: {e}")
    
    print("\n🔍 Running Django system check...")
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'check'])
    
except Exception as e:
    print(f"❌ Critical error: {e}")
    import traceback
    traceback.print_exc()
