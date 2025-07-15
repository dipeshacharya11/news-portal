from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count

from .serializers import NewsSerializer, CategorySerializer, NewsDetailSerializer

from mainsite.models import HomePageSettings
from news.models import Category, News


class HomePageApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            home_page_settings = HomePageSettings.objects.last()
            news_list = News.objects.filter(is_published=True)

            # Handle case when no homepage settings exist
            if not home_page_settings:
                categories = Category.objects.all()[:5]

                # Get latest news from different categories as fallback
                post_catalog_one = news_list.filter(category=categories[0]).order_by('-id')[:3] if categories else news_list.order_by('-id')[:3]
                post_catalog_two = news_list.filter(category=categories[1]).order_by('-id')[:2] if len(categories) > 1 else news_list.order_by('-id')[3:5]
                post_catalog_three = news_list.filter(category=categories[2]).order_by('-id')[:2] if len(categories) > 2 else news_list.order_by('-id')[5:7]
                post_catalog_four = news_list.filter(category=categories[3]).order_by('-id')[:3] if len(categories) > 3 else news_list.order_by('-id')[7:10]
                post_catalog_five = news_list.filter(category=categories[4]).order_by('-id')[:2] if len(categories) > 4 else news_list.order_by('-id')[10:12]

                # Get latest news as fallback for featured items
                latest_news = news_list.order_by('-id')[:3]
                hot_news = latest_news[0] if latest_news else None
                trending_new = latest_news[1] if len(latest_news) > 1 else None
                editor_choice = latest_news[2] if len(latest_news) > 2 else None
            else:
                # Normal case when homepage settings exist
                post_catalog_one = news_list.filter(
                    category=home_page_settings.post_catalog_one).order_by('-id')[:3] if home_page_settings.post_catalog_one else news_list.order_by('-id')[:3]
                post_catalog_two = news_list.filter(
                    category=home_page_settings.post_catalog_two).order_by('-id')[:2] if home_page_settings.post_catalog_two else news_list.order_by('-id')[3:5]
                post_catalog_three = news_list.filter(
                    category=home_page_settings.post_catalog_three).order_by('-id')[:2] if home_page_settings.post_catalog_three else news_list.order_by('-id')[5:7]
                post_catalog_four = news_list.filter(
                    category=home_page_settings.post_catalog_four).order_by('-id')[:3] if home_page_settings.post_catalog_four else news_list.order_by('-id')[7:10]
                post_catalog_five = news_list.filter(
                    category=home_page_settings.post_catalog_five).order_by('-id')[:2] if home_page_settings.post_catalog_five else news_list.order_by('-id')[10:12]

                hot_news = home_page_settings.hot_news
                trending_new = home_page_settings.trending
                editor_choice = home_page_settings.editor_choice

        except Exception as e:
            # Fallback in case of any error
            news_list = News.objects.filter(is_published=True)
            latest_news = news_list.order_by('-id')[:12]

            post_catalog_one = latest_news[:3]
            post_catalog_two = latest_news[3:5]
            post_catalog_three = latest_news[5:7]
            post_catalog_four = latest_news[7:10]
            post_catalog_five = latest_news[10:12]

            hot_news = latest_news[0] if latest_news else None
            trending_new = latest_news[1] if len(latest_news) > 1 else None
            editor_choice = latest_news[2] if len(latest_news) > 2 else None

        post_catalog_one = NewsSerializer(post_catalog_one, many=True)
        post_catalog_two = NewsSerializer(post_catalog_two, many=True)
        post_catalog_three = NewsSerializer(post_catalog_three, many=True)
        post_catalog_four = NewsSerializer(post_catalog_four, many=True)
        post_catalog_five = NewsSerializer(post_catalog_five, many=True)
        hot_news = NewsSerializer(hot_news)
        trending_new = NewsSerializer(trending_new)
        editor_choice = NewsSerializer(editor_choice)

        data = {
            'post_catalog_one': post_catalog_one.data,
            'post_catalog_two': post_catalog_two.data,
            'post_catalog_three': post_catalog_three.data,
            'post_catalog_four': post_catalog_four.data,
            'post_catalog_five': post_catalog_five.data,
            'hot_news': hot_news.data,
            'trending_new': trending_new.data,
            'editor_choice': editor_choice.data
        }

        return Response(data, status=status.HTTP_200_OK)


class CategoryApiView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = [AllowAny]


class SingleCategoryApiView(RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


@api_view(['GET'])
def NewsFilterByTag(request, tag):
    if request.method == 'GET':
        news_list = News.objects.filter(
            tags__name__in=[tag], is_published=True).order_by('-id')
        serializer = NewsSerializer(news_list, many=True)

        data = {
            'news': serializer.data,
            'tag': [tag],

        }
        return Response(data, status=status.HTTP_200_OK)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class PopularMostCommentedNewsApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):

        categories = Category.objects.all()[:6]
        news_list = News.objects.all()
        popular_news = news_list.filter(category=categories[0]).annotate(
            Count('post__id')).order_by('-id')
        most_commented = news_list.annotate(
            Count('post__id')).order_by('-post__id__count')[:4]

        popular_news = NewsSerializer(popular_news, many=True)
        most_commented = NewsSerializer(most_commented, many=True)

        data = {
            'popular_news': popular_news.data,
            'most_commented': most_commented.data,

        }

        return Response(data, status=status.HTTP_200_OK)


class BreakingNewsApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        """
        Get breaking news from multiple sources
        """
        try:
            # Get breaking news from News model
            breaking_news_items = News.objects.filter(
                is_published=True,
                is_breaking=True
            ).order_by('-timestamp')[:5]

            # Get breaking news from BreakingNews model
            from news.models import BreakingNews
            breaking_news_alerts = BreakingNews.objects.filter(
                is_active=True
            ).order_by('-created_at')[:3]

            # Serialize the data
            breaking_items_data = NewsSerializer(breaking_news_items, many=True).data

            # Format breaking news alerts
            breaking_alerts_data = []
            for alert in breaking_news_alerts:
                breaking_alerts_data.append({
                    'title': alert.title,
                    'content': alert.content,
                    'created_at': alert.created_at.isoformat(),
                    'is_valid': alert.is_valid()
                })

            # Combine all breaking news
            all_breaking_news = []

            # Add news items
            for item in breaking_items_data:
                all_breaking_news.append({
                    'title': item['title'],
                    'content': item['description'] or '',
                    'url': item.get('slug', ''),
                    'timestamp': item['timestamp'],
                    'source': 'news'
                })

            # Add breaking news alerts
            for alert in breaking_alerts_data:
                if alert['is_valid']:
                    all_breaking_news.append({
                        'title': alert['title'],
                        'content': alert['content'],
                        'url': '',
                        'timestamp': alert['created_at'],
                        'source': 'alert'
                    })

            # Sort by timestamp (newest first)
            all_breaking_news.sort(key=lambda x: x['timestamp'], reverse=True)

            data = {
                'status': 'success',
                'breaking_news': all_breaking_news[:5],  # Top 5 breaking news
                'count': len(all_breaking_news),
                'breaking_news_items': breaking_items_data,
                'breaking_alerts': breaking_alerts_data
            }

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e),
                'breaking_news': []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
