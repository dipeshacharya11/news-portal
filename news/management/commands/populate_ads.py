from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from news.models import Advertisement, BreakingNews, Newsletter


class Command(BaseCommand):
    help = 'Populate the database with sample advertisements and other content'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing ads before adding new ones',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing advertisements...')
            Advertisement.objects.all().delete()
            BreakingNews.objects.all().delete()

        self.stdout.write('Creating sample advertisements...')
        
        # Sample advertisements
        ads_data = [
            {
                'title': 'NBC News Premium Subscription',
                'ad_type': 'banner',
                'ad_size': '728x90',
                'html_content': '''
                <div style="background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; padding: 20px; text-align: center; border-radius: 8px;">
                    <h3 style="margin: 0; font-size: 24px;">Get NBC News Premium</h3>
                    <p style="margin: 10px 0; font-size: 16px;">Ad-free experience, exclusive content, and breaking news alerts</p>
                    <button style="background: white; color: #1e3a8a; border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold; cursor: pointer;">
                        Subscribe Now - $9.99/month
                    </button>
                </div>
                ''',
                'url': 'https://www.nbcnews.com/premium',
            },
            {
                'title': 'Tech Conference 2024',
                'ad_type': 'sidebar',
                'ad_size': '300x250',
                'html_content': '''
                <div style="background: #f8f9fa; border: 2px solid #e9ecef; padding: 15px; text-align: center; border-radius: 8px;">
                    <h4 style="color: #1e3a8a; margin-top: 0;">Tech Summit 2024</h4>
                    <p style="font-size: 14px; color: #6c757d;">Join industry leaders for the biggest tech event of the year</p>
                    <div style="background: #1e3a8a; color: white; padding: 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">
                        Early Bird: 50% OFF
                    </div>
                    <button style="background: #dc2626; color: white; border: none; padding: 8px 16px; border-radius: 4px; margin-top: 10px; cursor: pointer;">
                        Register Now
                    </button>
                </div>
                ''',
                'url': 'https://techsummit2024.com',
            },
            {
                'title': 'Financial Planning Services',
                'ad_type': 'banner',
                'ad_size': '970x250',
                'html_content': '''
                <div style="background: linear-gradient(135deg, #059669 0%, #10b981 100%); color: white; padding: 30px; text-align: center; border-radius: 8px; display: flex; align-items: center; justify-content: space-between;">
                    <div style="flex: 1;">
                        <h2 style="margin: 0; font-size: 28px;">Secure Your Financial Future</h2>
                        <p style="margin: 10px 0; font-size: 18px;">Expert financial planning and investment advice</p>
                    </div>
                    <div style="flex: 0 0 auto;">
                        <button style="background: white; color: #059669; border: none; padding: 15px 30px; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer;">
                            Free Consultation
                        </button>
                    </div>
                </div>
                ''',
                'url': 'https://financialplanning.com',
            },
            {
                'title': 'Mobile App Download',
                'ad_type': 'popup',
                'ad_size': '300x250',
                'html_content': '''
                <div style="background: white; padding: 20px; text-align: center; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">
                    <h3 style="color: #1e3a8a; margin-top: 0;">Download NBC News App</h3>
                    <p style="color: #6c757d; font-size: 14px;">Get breaking news alerts and stay informed on the go</p>
                    <div style="margin: 15px 0;">
                        <span style="background: #1e3a8a; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px;">⭐ 4.8 Rating</span>
                    </div>
                    <button style="background: #1e3a8a; color: white; border: none; padding: 12px 24px; border-radius: 6px; font-weight: bold; cursor: pointer; width: 100%;">
                        Download Free
                    </button>
                </div>
                ''',
                'url': 'https://apps.apple.com/nbcnews',
            },
            {
                'title': 'Online Education Platform',
                'ad_type': 'inline',
                'ad_size': '300x250',
                'html_content': '''
                <div style="background: #fef3c7; border: 2px solid #f59e0b; padding: 15px; border-radius: 8px;">
                    <h4 style="color: #92400e; margin-top: 0;">📚 Learn Something New Today</h4>
                    <p style="font-size: 14px; color: #78350f;">Thousands of courses from industry experts</p>
                    <ul style="font-size: 12px; color: #78350f; margin: 10px 0;">
                        <li>Business & Technology</li>
                        <li>Creative Arts & Design</li>
                        <li>Personal Development</li>
                    </ul>
                    <button style="background: #f59e0b; color: white; border: none; padding: 8px 16px; border-radius: 4px; font-weight: bold; cursor: pointer;">
                        Start Learning - Free Trial
                    </button>
                </div>
                ''',
                'url': 'https://onlinelearning.com',
            },
            {
                'title': 'Health & Wellness',
                'ad_type': 'sidebar',
                'ad_size': '160x600',
                'html_content': '''
                <div style="background: linear-gradient(180deg, #ec4899 0%, #be185d 100%); color: white; padding: 20px; text-align: center; border-radius: 8px; height: 580px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <h4 style="margin-top: 0;">💪 Health First</h4>
                        <p style="font-size: 12px;">Your wellness journey starts here</p>
                    </div>
                    <div>
                        <p style="font-size: 11px;">✓ Fitness Plans<br>✓ Nutrition Guides<br>✓ Mental Health Support</p>
                    </div>
                    <button style="background: white; color: #be185d; border: none; padding: 8px 12px; border-radius: 4px; font-size: 11px; font-weight: bold; cursor: pointer;">
                        Start Today
                    </button>
                </div>
                ''',
                'url': 'https://healthwellness.com',
            }
        ]

        # Create advertisements
        for ad_data in ads_data:
            # Random start and end dates
            start_date = timezone.now() - timedelta(days=random.randint(1, 10))
            end_date = timezone.now() + timedelta(days=random.randint(30, 90))
            
            ad = Advertisement.objects.create(
                title=ad_data['title'],
                ad_type=ad_data['ad_type'],
                ad_size=ad_data['ad_size'],
                html_content=ad_data['html_content'],
                url=ad_data['url'],
                is_active=True,
                start_date=start_date,
                end_date=end_date,
                clicks=random.randint(10, 500),
                impressions=random.randint(1000, 10000)
            )
            
            self.stdout.write(f'Created advertisement: {ad.title}')

        # Create breaking news
        breaking_news_data = [
            {
                'title': 'LIVE: Major Economic Summit in Progress',
                'content': 'World leaders are currently meeting to discuss global economic policies and climate change initiatives.',
            },
            {
                'title': 'URGENT: Weather Alert Issued for Multiple States',
                'content': 'Severe weather conditions expected across the region. Residents advised to take necessary precautions.',
            }
        ]

        for news_data in breaking_news_data:
            breaking_news = BreakingNews.objects.create(
                title=news_data['title'],
                content=news_data['content'],
                is_active=True,
                expires_at=timezone.now() + timedelta(hours=24)
            )
            self.stdout.write(f'Created breaking news: {breaking_news.title}')

        # Create sample newsletter subscriptions
        sample_emails = [
            'user1@example.com',
            'user2@example.com',
            'subscriber@test.com',
            'news.lover@email.com',
            'reader@sample.org'
        ]

        for email in sample_emails:
            newsletter, created = Newsletter.objects.get_or_create(
                email=email,
                defaults={'is_active': True}
            )
            if created:
                self.stdout.write(f'Created newsletter subscription: {email}')

        self.stdout.write(
            self.style.SUCCESS('Successfully populated advertisements and breaking news!')
        )
