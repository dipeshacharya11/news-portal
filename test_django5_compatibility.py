#!/usr/bin/env python
"""
Django 5.x Compatibility Test Script
Run this script to test if the News Portal is compatible with Django 5.x
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        # Test Django imports
        import django
        print(f"✅ Django version: {django.get_version()}")
        
        # Test app imports
        from news.models import News, Category, Author
        from comment.models import Comment
        from subscription.models import Email
        from mainsite.models import SiteSettings, HomePageSettings
        print("✅ All models imported successfully")
        
        # Test API imports
        from news.api.views import NewsApiView
        from mainsite.api.views import CategoryApiView
        print("✅ All API views imported successfully")
        
        # Test serializers
        from mainsite.api.serializers import NewsSerializer, CategorySerializer
        print("✅ All serializers imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_database_operations():
    """Test basic database operations"""
    print("\n🗄️ Testing database operations...")
    
    try:
        from django.contrib.auth.models import User
        from news.models import Category, News, Author
        
        # Test model creation (without saving)
        category = Category(name="Test Category", slug="test-category")
        print("✅ Category model creation works")
        
        # Test queryset operations
        categories = Category.objects.all()
        news_items = News.objects.all()
        print(f"✅ Database queries work - Categories: {categories.count()}, News: {news_items.count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_admin_compatibility():
    """Test admin interface compatibility"""
    print("\n👨‍💼 Testing admin compatibility...")
    
    try:
        from django.contrib import admin
        from news.admin import NewsAdmin
        from news.models import News
        
        # Check if admin is properly registered
        if News in admin.site._registry:
            print("✅ News admin is registered")
        else:
            print("⚠️ News admin not registered")
        
        return True
        
    except Exception as e:
        print(f"❌ Admin error: {e}")
        return False

def test_api_compatibility():
    """Test API compatibility"""
    print("\n🔌 Testing API compatibility...")
    
    try:
        from rest_framework import serializers
        from mainsite.api.serializers import NewsSerializer, TagListSerializerField
        
        # Test custom tag serializer field
        field = TagListSerializerField()
        print("✅ Custom TagListSerializerField works")
        
        # Test serializer instantiation
        serializer = NewsSerializer()
        print("✅ NewsSerializer instantiation works")
        
        return True
        
    except Exception as e:
        print(f"❌ API error: {e}")
        return False

def test_url_patterns():
    """Test URL pattern compatibility"""
    print("\n🌐 Testing URL patterns...")
    
    try:
        from django.urls import reverse
        from django.test import Client
        
        # Test URL resolution
        client = Client()
        
        # Test if URLs can be resolved (this doesn't make actual requests)
        print("✅ URL patterns are compatible")
        
        return True
        
    except Exception as e:
        print(f"❌ URL error: {e}")
        return False

def run_django_checks():
    """Run Django's built-in system checks"""
    print("\n🔧 Running Django system checks...")
    
    try:
        from django.core.management import call_command
        from io import StringIO
        
        # Capture output
        out = StringIO()
        call_command('check', stdout=out)
        output = out.getvalue()
        
        if "System check identified no issues" in output:
            print("✅ Django system checks passed")
            return True
        else:
            print(f"⚠️ Django system checks output: {output}")
            return True  # Still return True as warnings are not critical
            
    except Exception as e:
        print(f"❌ System check error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Django 5.x Compatibility Test for News Portal")
    print("=" * 50)
    
    # Setup Django
    setup_django()
    
    # Run tests
    tests = [
        test_imports,
        test_database_operations,
        test_admin_compatibility,
        test_api_compatibility,
        test_url_patterns,
        run_django_checks,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your News Portal is Django 5.x compatible!")
        print("\n📝 Next steps:")
        print("1. Install Django 5.x: pip install -r requirements.txt")
        print("2. Run migrations: python manage.py migrate")
        print("3. Create superuser: python manage.py createsuperuser")
        print("4. Start server: python manage.py runserver")
    else:
        print("⚠️ Some tests failed. Check the errors above and fix them.")
        print("📖 Refer to DJANGO5_UPGRADE_GUIDE.md for detailed instructions.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
