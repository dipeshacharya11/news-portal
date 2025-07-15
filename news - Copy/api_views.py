"""
API Views for News Data Integration
Provides endpoints for fetching and managing news from external APIs
"""

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
import json
import logging

logger = logging.getLogger('news_api')

class NewsAPIView(View):
    """Base API view for news operations"""
    
    def dispatch(self, request, *args, **kwargs):
        # Add CORS headers
        response = super().dispatch(request, *args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

@method_decorator(csrf_exempt, name='dispatch')
class FetchNewsAPIView(NewsAPIView):
    """API endpoint to fetch news from NewsData.io"""
    
    def get(self, request):
        """Get news articles with optional filtering"""
        try:
            # Import here to avoid circular imports
            from news.services import news_service
            
            # Get query parameters
            category = request.GET.get('category', 'top')
            size = min(int(request.GET.get('size', 10)), 50)
            breaking_only = request.GET.get('breaking', '').lower() == 'true'
            
            if breaking_only:
                articles = news_service.fetch_breaking_news()
            else:
                articles = news_service.fetch_latest_news(
                    category=category,
                    size=size
                )
            
            return JsonResponse({
                'status': 'success',
                'count': len(articles),
                'articles': articles,
                'category': category,
                'breaking_only': breaking_only
            })
            
        except Exception as e:
            logger.error(f"Error fetching news: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    def post(self, request):
        """Trigger news fetch and save to database"""
        try:
            # Import here to avoid circular imports
            from news.management.commands.fetch_news import Command
            from io import StringIO
            import sys
            
            # Parse request data
            data = json.loads(request.body) if request.body else {}
            category = data.get('category')
            breaking_only = data.get('breaking_only', False)
            size = min(int(data.get('size', 20)), 50)
            
            # Capture command output
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()
            
            try:
                # Create and run command
                command = Command()

                # Get or create default author (same logic as in the command)
                from django.contrib.auth.models import User
                from news.models import Author

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

                if breaking_only:
                    command.fetch_breaking_news(default_author)
                elif category:
                    command.fetch_category_news(category, default_author, size)
                else:
                    command.fetch_all_categories(default_author, size)
                
                output = captured_output.getvalue()
                
            finally:
                sys.stdout = old_stdout
            
            return JsonResponse({
                'status': 'success',
                'message': 'News fetch completed',
                'output': output,
                'category': category,
                'breaking_only': breaking_only,
                'size': size
            })
            
        except Exception as e:
            logger.error(f"Error in news fetch command: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class NewsSearchAPIView(NewsAPIView):
    """API endpoint for searching news"""
    
    def get(self, request):
        """Search news articles"""
        try:
            from news.services import news_service
            
            query = request.GET.get('q', '')
            size = min(int(request.GET.get('size', 10)), 50)
            
            if not query:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Query parameter "q" is required'
                }, status=400)
            
            articles = news_service.search_news(query, size)
            
            return JsonResponse({
                'status': 'success',
                'count': len(articles),
                'articles': articles,
                'query': query
            })
            
        except Exception as e:
            logger.error(f"Error searching news: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

@method_decorator(staff_member_required, name='dispatch')
class APIStatusView(NewsAPIView):
    """API endpoint to check NewsData.io API status"""
    
    def get(self, request):
        """Get API status and usage information"""
        try:
            from news.services import news_service
            
            status = news_service.get_api_status()
            
            return JsonResponse({
                'status': 'success',
                'api_status': status,
                'settings': {
                    'base_url': settings.NEWSDATA_BASE_URL,
                    'default_categories': settings.DEFAULT_NEWS_CATEGORIES,
                    'default_language': settings.DEFAULT_NEWS_LANGUAGE,
                    'default_country': settings.DEFAULT_NEWS_COUNTRY,
                    'cache_timeout': settings.NEWS_CACHE_TIMEOUT,
                    'breaking_cache_timeout': settings.BREAKING_NEWS_CACHE_TIMEOUT,
                }
            })
            
        except Exception as e:
            logger.error(f"Error getting API status: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

# Function-based views for simpler endpoints
@require_http_methods(["GET"])
def breaking_news_api(request):
    """Simple endpoint for breaking news"""
    try:
        from news.services import news_service
        
        articles = news_service.fetch_breaking_news()
        
        return JsonResponse({
            'status': 'success',
            'breaking_news': articles[:5],  # Top 5 breaking news
            'count': len(articles)
        })
        
    except Exception as e:
        logger.error(f"Error fetching breaking news: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Unable to fetch breaking news'
        }, status=500)

@require_http_methods(["GET"])
def categories_api(request):
    """Get available news categories"""
    return JsonResponse({
        'status': 'success',
        'categories': [
            {'id': 'top', 'name': 'Top Stories', 'description': 'Most important news'},
            {'id': 'politics', 'name': 'Politics', 'description': 'Political news and updates'},
            {'id': 'technology', 'name': 'Technology', 'description': 'Tech news and innovations'},
            {'id': 'business', 'name': 'Business', 'description': 'Business and finance news'},
            {'id': 'sports', 'name': 'Sports', 'description': 'Sports news and updates'},
            {'id': 'world', 'name': 'World News', 'description': 'International news'},
            {'id': 'health', 'name': 'Health', 'description': 'Health and medical news'},
            {'id': 'entertainment', 'name': 'Entertainment', 'description': 'Entertainment news'},
            {'id': 'science', 'name': 'Science', 'description': 'Science and research news'},
            {'id': 'environment', 'name': 'Environment', 'description': 'Environmental news'},
        ]
    })

@require_http_methods(["POST"])
@csrf_exempt
def refresh_cache_api(request):
    """Clear news cache to force refresh"""
    try:
        from django.core.cache import cache
        
        # Clear specific news-related cache keys
        cache_keys = [
            'breaking_news',
            'latest_news_*',
            'search_news_*',
            'newsdata_requests_*'
        ]
        
        # In a real implementation, you'd want to be more selective
        cache.clear()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Cache cleared successfully'
        })
        
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
