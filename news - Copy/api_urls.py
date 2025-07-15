"""
API URL patterns for News Data Integration
"""

from django.urls import path
from . import api_views

app_name = 'news_api'

urlpatterns = [
    # News fetching endpoints
    path('fetch/', api_views.FetchNewsAPIView.as_view(), name='fetch_news'),
    path('search/', api_views.NewsSearchAPIView.as_view(), name='search_news'),
    path('breaking/', api_views.breaking_news_api, name='breaking_news'),
    
    # Configuration endpoints
    path('categories/', api_views.categories_api, name='categories'),
    path('status/', api_views.APIStatusView.as_view(), name='api_status'),
    
    # Utility endpoints
    path('refresh-cache/', api_views.refresh_cache_api, name='refresh_cache'),
]
