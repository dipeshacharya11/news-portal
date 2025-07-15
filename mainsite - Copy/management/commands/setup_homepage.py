from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from news.models import News, Category, Author
from mainsite.models import HomePageSettings


class Command(BaseCommand):
    help = 'Setup homepage settings with default data'

    def handle(self, *args, **options):
        self.stdout.write('Setting up homepage...')
        
        # Create basic categories if they don't exist
        categories_data = [
            "Politics", "Technology", "Sports", "Business", "World News"
        ]
        
        categories = []
        for cat_name in categories_data:
            category, created = Category.objects.get_or_create(name=cat_name)
            categories.append(category)
            if created:
                self.stdout.write(f"Created category: {cat_name}")
        
        # Create a default user and author if they don't exist
        user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write("Created admin user")
        
        author, created = Author.objects.get_or_create(user=user)
        if created:
            self.stdout.write("Created author")
        
        # Get existing news or create sample news
        existing_news = list(News.objects.filter(is_published=True)[:5])
        
        if not existing_news:
            sample_news = [
                {
                    'title': 'Breaking: Major Political Development',
                    'description': 'Important political news that affects everyone.',
                    'content': 'This is a detailed article about the political development...',
                    'category': categories[0],  # Politics
                    'is_breaking': True,
                    'is_featured': True
                },
                {
                    'title': 'Tech Innovation Breakthrough',
                    'description': 'New technology changes the industry.',
                    'content': 'This article discusses the latest technology breakthrough...',
                    'category': categories[1],  # Technology
                    'is_trending': True
                },
                {
                    'title': 'Sports Championship Results',
                    'description': 'Latest results from the championship.',
                    'content': 'Coverage of the recent sports championship...',
                    'category': categories[2],  # Sports
                },
            ]
            
            for news_data in sample_news:
                news = News.objects.create(
                    author=author,
                    title=news_data['title'],
                    description=news_data['description'],
                    content=news_data['content'],
                    category=news_data['category'],
                    is_published=True,
                    is_breaking=news_data.get('is_breaking', False),
                    is_featured=news_data.get('is_featured', False),
                    is_trending=news_data.get('is_trending', False)
                )
                existing_news.append(news)
                self.stdout.write(f"Created news: {news.title}")
        
        # Create or update homepage settings
        homepage_settings, created = HomePageSettings.objects.get_or_create(
            id=1,
            defaults={
                'hot_news': existing_news[0] if existing_news else None,
                'trending': existing_news[1] if len(existing_news) > 1 else None,
                'editor_choice': existing_news[2] if len(existing_news) > 2 else None,
                'post_catalog_one': categories[0],
                'post_catalog_two': categories[1],
                'post_catalog_three': categories[2],
                'post_catalog_four': categories[3],
                'post_catalog_five': categories[4],
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS("Created homepage settings"))
        else:
            # Update existing settings to ensure they have valid references
            if existing_news:
                homepage_settings.hot_news = existing_news[0]
                if len(existing_news) > 1:
                    homepage_settings.trending = existing_news[1]
                if len(existing_news) > 2:
                    homepage_settings.editor_choice = existing_news[2]
            
            homepage_settings.post_catalog_one = categories[0]
            homepage_settings.post_catalog_two = categories[1]
            homepage_settings.post_catalog_three = categories[2]
            homepage_settings.post_catalog_four = categories[3]
            homepage_settings.post_catalog_five = categories[4]
            homepage_settings.save()
            self.stdout.write(self.style.SUCCESS("Updated homepage settings"))
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Homepage setup completed! '
                f'Categories: {len(categories)}, '
                f'News items: {News.objects.count()}'
            )
        )
