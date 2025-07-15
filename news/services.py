"""
NewsData.io API Integration Service
Handles fetching real news data from NewsData.io API
"""

import requests
import logging
from datetime import datetime, timedelta
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone
from typing import Dict, List, Optional
import time

logger = logging.getLogger('news_api')

class NewsDataService:
    """Service class for interacting with NewsData.io API"""
    
    def __init__(self):
        self.api_key = settings.NEWSDATA_API_KEY
        self.base_url = settings.NEWSDATA_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'X-ACCESS-KEY': self.api_key,
            'User-Agent': 'NBC-News-Portal/1.0'
        })
        
        # Rate limiting
        self.requests_per_hour = settings.NEWSDATA_REQUESTS_PER_HOUR
        self.requests_per_day = settings.NEWSDATA_REQUESTS_PER_DAY
        
    def _check_rate_limit(self) -> bool:
        """Check if we're within API rate limits"""
        current_hour = datetime.now().strftime('%Y-%m-%d-%H')
        current_day = datetime.now().strftime('%Y-%m-%d')
        
        hourly_key = f'newsdata_requests_hour_{current_hour}'
        daily_key = f'newsdata_requests_day_{current_day}'
        
        hourly_count = cache.get(hourly_key, 0)
        daily_count = cache.get(daily_key, 0)
        
        if hourly_count >= self.requests_per_hour:
            logger.warning(f"Hourly rate limit exceeded: {hourly_count}/{self.requests_per_hour}")
            return False
            
        if daily_count >= self.requests_per_day:
            logger.warning(f"Daily rate limit exceeded: {daily_count}/{self.requests_per_day}")
            return False
            
        return True
    
    def _increment_rate_limit(self):
        """Increment rate limit counters"""
        current_hour = datetime.now().strftime('%Y-%m-%d-%H')
        current_day = datetime.now().strftime('%Y-%m-%d')
        
        hourly_key = f'newsdata_requests_hour_{current_hour}'
        daily_key = f'newsdata_requests_day_{current_day}'
        
        # Increment counters with expiration
        cache.set(hourly_key, cache.get(hourly_key, 0) + 1, 3600)  # 1 hour
        cache.set(daily_key, cache.get(daily_key, 0) + 1, 86400)   # 24 hours
    
    def _make_request(self, params: Dict) -> Optional[Dict]:
        """Make API request with error handling and rate limiting"""
        if not self.api_key:
            logger.error("NewsData.io API key not configured")
            return None
            
        if not self._check_rate_limit():
            logger.warning("Rate limit exceeded, skipping API request")
            return None
        
        try:
            response = self.session.get(self.base_url, params=params, timeout=30)
            self._increment_rate_limit()
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    logger.info(f"Successfully fetched {len(data.get('results', []))} articles")
                    return data
                else:
                    logger.error(f"API error: {data.get('message', 'Unknown error')}")
                    return None
            else:
                logger.error(f"HTTP error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return None
    
    def fetch_latest_news(self, 
                         category: str = None, 
                         country: str = None, 
                         language: str = None,
                         size: int = 10) -> List[Dict]:
        """Fetch latest news articles"""
        
        cache_key = f'latest_news_{category}_{country}_{language}_{size}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info(f"Returning cached news data for {cache_key}")
            return cached_data
        
        params = {
            'language': language or settings.DEFAULT_NEWS_LANGUAGE,
            'size': min(size, 50),  # API limit
        }
        
        if category and category != 'top':
            params['category'] = category
            
        if country:
            params['country'] = country
        
        data = self._make_request(params)
        
        if data and data.get('results'):
            articles = self._process_articles(data['results'])
            cache.set(cache_key, articles, settings.NEWS_CACHE_TIMEOUT)
            return articles
        
        return []
    
    def fetch_breaking_news(self) -> List[Dict]:
        """Fetch breaking/urgent news"""
        cache_key = 'breaking_news'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        # Fetch top news from multiple high-priority categories
        breaking_categories = ['top', 'politics', 'world']
        all_breaking = []
        
        for category in breaking_categories:
            params = {
                'category': category if category != 'top' else None,
                'language': settings.DEFAULT_NEWS_LANGUAGE,
                'country': settings.DEFAULT_NEWS_COUNTRY,
                'size': 5,
                'prioritydomain': 'top'  # Get from top domains
            }
            
            # Remove None values
            params = {k: v for k, v in params.items() if v is not None}
            
            data = self._make_request(params)
            if data and data.get('results'):
                articles = self._process_articles(data['results'])
                all_breaking.extend(articles)
                
            # Small delay between requests
            time.sleep(0.5)
        
        # Remove duplicates and sort by publication time
        unique_articles = []
        seen_titles = set()
        
        for article in all_breaking:
            if article['title'] not in seen_titles:
                unique_articles.append(article)
                seen_titles.add(article['title'])
        
        # Sort by publication time (newest first)
        unique_articles.sort(key=lambda x: x['pubDate'], reverse=True)
        breaking_news = unique_articles[:10]  # Top 10 breaking news
        
        cache.set(cache_key, breaking_news, settings.BREAKING_NEWS_CACHE_TIMEOUT)
        return breaking_news
    
    def search_news(self, query: str, size: int = 10) -> List[Dict]:
        """Search for news articles by query"""
        cache_key = f'search_news_{query}_{size}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        params = {
            'q': query,
            'language': settings.DEFAULT_NEWS_LANGUAGE,
            'size': min(size, 50),
        }
        
        data = self._make_request(params)
        
        if data and data.get('results'):
            articles = self._process_articles(data['results'])
            cache.set(cache_key, articles, settings.NEWS_CACHE_TIMEOUT)
            return articles
        
        return []
    
    def _process_articles(self, articles: List[Dict]) -> List[Dict]:
        """Process and clean article data"""
        processed = []
        
        for article in articles:
            try:
                # Safely get and clean article data
                title = article.get('title', '') or ''
                description = article.get('description', '') or ''
                content = article.get('content', '') or ''

                processed_article = {
                    'title': title.strip() if title else '',
                    'description': description.strip() if description else '',
                    'content': content.strip() if content else '',
                    'url': article.get('link', '') or '',
                    'image_url': article.get('image_url', '') or '',
                    'source': article.get('source_id', '') or '',
                    'source_name': article.get('source_name', '') or '',
                    'author': ', '.join(article.get('creator', [])) if article.get('creator') else '',
                    'pubDate': article.get('pubDate', '') or '',
                    'category': ', '.join(article.get('category', [])) if article.get('category') else '',
                    'country': ', '.join(article.get('country', [])) if article.get('country') else '',
                    'language': article.get('language', '') or '',
                    'keywords': ', '.join(article.get('keywords', [])) if article.get('keywords') else '',
                }
                
                # Skip articles with missing essential data
                if processed_article['title'] and processed_article['url']:
                    processed.append(processed_article)
                    
            except Exception as e:
                logger.warning(f"Error processing article: {str(e)}")
                continue
        
        return processed
    
    def get_api_status(self) -> Dict:
        """Get API status and usage information"""
        current_hour = datetime.now().strftime('%Y-%m-%d-%H')
        current_day = datetime.now().strftime('%Y-%m-%d')
        
        hourly_key = f'newsdata_requests_hour_{current_hour}'
        daily_key = f'newsdata_requests_day_{current_day}'
        
        return {
            'api_key_configured': bool(self.api_key),
            'hourly_requests': cache.get(hourly_key, 0),
            'hourly_limit': self.requests_per_hour,
            'daily_requests': cache.get(daily_key, 0),
            'daily_limit': self.requests_per_day,
            'cache_timeout': settings.NEWS_CACHE_TIMEOUT,
            'breaking_cache_timeout': settings.BREAKING_NEWS_CACHE_TIMEOUT,
        }

# Global instance
news_service = NewsDataService()
