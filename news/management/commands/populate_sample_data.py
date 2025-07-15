from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta
import random

from news.models import Category, News, Author, Advertisement, BreakingNews, Newsletter

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the database with sample content for NBC News Portal'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before adding new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            News.objects.all().delete()
            Category.objects.all().delete()
            Author.objects.all().delete()
            Advertisement.objects.all().delete()
            BreakingNews.objects.all().delete()
            Newsletter.objects.all().delete()

        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories_data = [
            {'name': 'Politics', 'slug': 'politics'},
            {'name': 'World News', 'slug': 'world-news'},
            {'name': 'Business', 'slug': 'business'},
            {'name': 'Technology', 'slug': 'technology'},
            {'name': 'Sports', 'slug': 'sports'},
            {'name': 'Entertainment', 'slug': 'entertainment'},
            {'name': 'Health', 'slug': 'health'},
            {'name': 'Science', 'slug': 'science'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'slug': cat_data['slug']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create sample users and authors
        users_data = [
            {'username': 'john_reporter', 'email': 'john@nbcnews.com', 'first_name': 'John', 'last_name': 'Smith'},
            {'username': 'sarah_journalist', 'email': 'sarah@nbcnews.com', 'first_name': 'Sarah', 'last_name': 'Johnson'},
            {'username': 'mike_editor', 'email': 'mike@nbcnews.com', 'first_name': 'Mike', 'last_name': 'Wilson'},
            {'username': 'lisa_correspondent', 'email': 'lisa@nbcnews.com', 'first_name': 'Lisa', 'last_name': 'Brown'},
        ]
        
        authors = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            
            author, created = Author.objects.get_or_create(user=user)
            authors.append(author)
            if created:
                self.stdout.write(f'Created author: {author.user.get_full_name()}')

        # Sample news articles
        news_data = [
            {
                'title': 'Breaking: Major Economic Summit Concludes with Historic Agreement',
                'description': 'World leaders reach unprecedented consensus on climate and economic policies.',
                'content': 'In a historic turn of events, the Global Economic Summit has concluded with a groundbreaking agreement that promises to reshape international trade and climate policies. The three-day summit, attended by leaders from over 50 nations, focused on sustainable economic growth and environmental protection.',
                'category': 'Politics',
                'is_breaking': True,
                'is_featured': True,
                'priority': 'breaking'
            },
            {
                'title': 'Tech Giants Announce Revolutionary AI Partnership',
                'description': 'Leading technology companies join forces to develop next-generation artificial intelligence.',
                'content': 'Major technology corporations have announced a groundbreaking partnership to advance artificial intelligence research and development. This collaboration aims to create more ethical and accessible AI technologies.',
                'category': 'Technology',
                'is_featured': True,
                'priority': 'high'
            },
            {
                'title': 'Olympic Games Set New Viewership Records',
                'description': 'This year\'s Olympic Games have attracted the largest global audience in history.',
                'content': 'The current Olympic Games have shattered all previous viewership records, with billions of viewers tuning in from around the world. The games have featured spectacular performances and inspiring stories of athletic achievement.',
                'category': 'Sports',
                'is_trending': True,
                'priority': 'normal'
            },
            {
                'title': 'Medical Breakthrough: New Treatment Shows Promise',
                'description': 'Researchers announce significant progress in treating a major disease.',
                'content': 'Medical researchers have announced a significant breakthrough in treating a previously incurable condition. The new treatment has shown remarkable success in clinical trials.',
                'category': 'Health',
                'is_featured': True,
                'priority': 'high'
            },
            {
                'title': 'Space Mission Discovers Potentially Habitable Planet',
                'description': 'NASA\'s latest space mission has identified a planet with conditions suitable for life.',
                'content': 'NASA scientists have announced the discovery of an exoplanet located in the habitable zone of its star system. This finding represents a major step forward in the search for extraterrestrial life.',
                'category': 'Science',
                'is_trending': True,
                'priority': 'high'
            },
            {
                'title': 'Global Markets React to New Trade Policies',
                'description': 'International markets show mixed reactions to recently announced trade agreements.',
                'content': 'Financial markets around the world are responding to new international trade policies announced this week. Analysts are closely monitoring the impact on various sectors.',
                'category': 'Business',
                'priority': 'normal'
            },
            {
                'title': 'Climate Change Summit Addresses Urgent Environmental Concerns',
                'description': 'World leaders gather to discuss immediate action on climate change.',
                'content': 'The annual Climate Change Summit has brought together environmental experts and world leaders to address the most pressing environmental challenges facing our planet.',
                'category': 'World News',
                'priority': 'high'
            },
            {
                'title': 'Entertainment Industry Embraces New Streaming Technologies',
                'description': 'Major studios announce adoption of cutting-edge streaming platforms.',
                'content': 'The entertainment industry is undergoing a major transformation as studios embrace new streaming technologies and distribution methods.',
                'category': 'Entertainment',
                'priority': 'normal'
            }
        ]

        # Create news articles
        for i, article_data in enumerate(news_data):
            category = Category.objects.get(name=article_data['category'])
            author = random.choice(authors)
            
            # Create realistic timestamps
            days_ago = random.randint(0, 30)
            timestamp = timezone.now() - timedelta(days=days_ago)
            
            news = News.objects.create(
                title=article_data['title'],
                slug=slugify(article_data['title']),
                description=article_data['description'],
                content=article_data['content'],
                author=author,
                category=category,
                is_published=True,
                is_breaking=article_data.get('is_breaking', False),
                is_featured=article_data.get('is_featured', False),
                is_trending=article_data.get('is_trending', False),
                priority=article_data.get('priority', 'normal'),
                views_count=random.randint(100, 5000),
                timestamp=timestamp,
                publish_date=timestamp
            )
            
            # Add some tags
            tags = ['news', 'breaking', 'important', 'trending', 'latest']
            news.tags.add(*random.sample(tags, random.randint(1, 3)))
            
            self.stdout.write(f'Created news article: {news.title}')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated sample content!')
        )
