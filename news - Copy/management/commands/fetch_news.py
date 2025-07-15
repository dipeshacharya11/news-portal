"""
Management command to fetch news from NewsData.io API
Usage: python manage.py fetch_news [--category=politics] [--breaking-only]
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone
from django.db import models
from news.services import news_service
from news.models import News, Category, Author
from django.contrib.auth.models import User
import logging

logger = logging.getLogger('news_api')

class Command(BaseCommand):
    help = 'Fetch news articles from NewsData.io API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--category',
            type=str,
            help='Specific category to fetch (e.g., politics, technology, sports)',
        )
        parser.add_argument(
            '--breaking-only',
            action='store_true',
            help='Fetch only breaking news',
        )
        parser.add_argument(
            '--size',
            type=int,
            default=20,
            help='Number of articles to fetch (default: 20, max: 50)',
        )
        parser.add_argument(
            '--force-refresh',
            action='store_true',
            help='Force refresh by clearing cache',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Starting NewsData.io API fetch...')
        )
        
        # Check API configuration
        api_status = news_service.get_api_status()
        if not api_status['api_key_configured']:
            raise CommandError(
                '❌ NewsData.io API key not configured. '
                'Please set NEWSDATA_API_KEY in your .env file.'
            )
        
        self.stdout.write(f"📊 API Status:")
        self.stdout.write(f"   Hourly requests: {api_status['hourly_requests']}/{api_status['hourly_limit']}")
        self.stdout.write(f"   Daily requests: {api_status['daily_requests']}/{api_status['daily_limit']}")
        
        # Clear cache if requested
        if options['force_refresh']:
            from django.core.cache import cache
            cache.clear()
            self.stdout.write(self.style.WARNING('🗑️  Cache cleared'))
        
        # Get or create default author
        default_user, created = User.objects.get_or_create(
            username='newsdata_api',
            defaults={
                'email': 'api@newsdata.io',
                'first_name': 'NewsData',
                'last_name': 'API',
                'is_staff': False,
                'is_active': True
            }
        )
        
        default_author, created = Author.objects.get_or_create(
            user=default_user
        )
        
        if options['breaking_only']:
            self.fetch_breaking_news(default_author)
        elif options['category']:
            self.fetch_category_news(options['category'], default_author, options['size'])
        else:
            self.fetch_all_categories(default_author, options['size'])
        
        self.stdout.write(
            self.style.SUCCESS('✅ News fetch completed successfully!')
        )

    def fetch_breaking_news(self, author):
        """Fetch breaking news"""
        self.stdout.write('🚨 Fetching breaking news...')
        
        articles = news_service.fetch_breaking_news()
        
        if not articles:
            self.stdout.write(self.style.WARNING('⚠️  No breaking news found'))
            return
        
        created_count = 0
        updated_count = 0
        
        for article_data in articles:
            created, updated = self.create_or_update_news(article_data, author, is_breaking=True)
            if created:
                created_count += 1
            elif updated:
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'🚨 Breaking News: {created_count} created, {updated_count} updated'
            )
        )

    def fetch_category_news(self, category, author, size):
        """Fetch news for specific category"""
        self.stdout.write(f'📰 Fetching {category} news...')
        
        articles = news_service.fetch_latest_news(
            category=category,
            size=size
        )
        
        if not articles:
            self.stdout.write(self.style.WARNING(f'⚠️  No {category} news found'))
            return
        
        created_count = 0
        updated_count = 0
        
        for article_data in articles:
            created, updated = self.create_or_update_news(article_data, author)
            if created:
                created_count += 1
            elif updated:
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'📰 {category.title()}: {created_count} created, {updated_count} updated'
            )
        )

    def fetch_all_categories(self, author, size):
        """Fetch news for all configured categories"""
        categories = settings.DEFAULT_NEWS_CATEGORIES
        total_created = 0
        total_updated = 0
        
        for category in categories:
            self.stdout.write(f'📰 Fetching {category} news...')
            
            articles = news_service.fetch_latest_news(
                category=category,
                size=size // len(categories)  # Distribute requests across categories
            )
            
            if not articles:
                self.stdout.write(self.style.WARNING(f'⚠️  No {category} news found'))
                continue
            
            created_count = 0
            updated_count = 0
            
            for article_data in articles:
                created, updated = self.create_or_update_news(article_data, author)
                if created:
                    created_count += 1
                elif updated:
                    updated_count += 1
            
            total_created += created_count
            total_updated += updated_count
            
            self.stdout.write(
                f'   ✅ {category.title()}: {created_count} created, {updated_count} updated'
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'📊 Total: {total_created} created, {total_updated} updated'
            )
        )

    def create_or_update_news(self, article_data, author, is_breaking=False):
        """Create or update news article"""
        try:
            # Get or create category
            category_name = article_data.get('category', 'General').split(',')[0].strip()
            if not category_name or category_name.lower() == 'top':
                category_name = 'General'

            category, created = Category.objects.get_or_create(
                name=category_name.title()
            )
            
            # Check if article already exists (by title only since we don't have source_url field)
            existing_news = News.objects.filter(
                title=article_data['title']
            ).first()
            
            if existing_news:
                # Update existing article
                updated = False
                if existing_news.description != article_data['description']:
                    existing_news.description = article_data['description']
                    updated = True
                
                if existing_news.content != article_data['content']:
                    existing_news.content = article_data['content']
                    updated = True
                
                if is_breaking and not existing_news.is_breaking:
                    existing_news.is_breaking = True
                    updated = True
                
                if updated:
                    existing_news.save()
                    return False, True
                
                return False, False
            
            # Create new article
            news = News.objects.create(
                title=article_data['title'][:250],  # Limit title length to model max
                description=article_data['description'] if article_data['description'] else article_data['title'],
                content=article_data['content'] if article_data['content'] else article_data['description'],
                author=author,
                category=category,
                thumbnail_url=article_data['image_url'],
                is_published=True,
                is_breaking=is_breaking,
                is_featured=is_breaking,  # Breaking news is featured
                priority='high' if is_breaking else 'normal',
            )

            # Add tags if available
            if article_data['keywords']:
                # Split keywords and add as tags
                keywords = article_data['keywords'].split(',')[:5]  # Limit to 5 tags
                for keyword in keywords:
                    keyword = keyword.strip()
                    if keyword:
                        news.tags.add(keyword)
            
            return True, False
            
        except Exception as e:
            logger.error(f"Error creating/updating news: {str(e)}")
            self.stdout.write(
                self.style.ERROR(f'❌ Error processing article: {str(e)}')
            )
            return False, False
