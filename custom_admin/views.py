from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.db.models import Count, Q, Sum
from django.utils import timezone
from django.utils.text import slugify
from django.contrib import messages
from datetime import timedelta
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST

from news.models import News, Category, Author, Advertisement, BreakingNews, Newsletter
from comment.models import Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


class DashboardView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'custom_admin/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Basic stats
        context['total_news'] = News.objects.count()
        context['published_news'] = News.objects.filter(is_published=True).count()
        context['total_users'] = User.objects.count()
        context['total_comments'] = Comment.objects.count()
        
        # Recent activity
        context['recent_news'] = News.objects.order_by('-timestamp')[:5]
        context['recent_comments'] = Comment.objects.order_by('-timestamp')[:5]
        
        # Breaking news
        context['breaking_news'] = BreakingNews.objects.filter(is_active=True)[:3]
        
        # Popular categories
        context['popular_categories'] = Category.objects.annotate(
            news_count=Count('category')
        ).order_by('-news_count')[:5]
        
        return context


class AnalyticsView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'custom_admin/analytics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Date range for analytics (last 30 days)
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)

        # News analytics
        context['news_by_category'] = Category.objects.annotate(
            count=Count('category')
        ).values('name', 'count')

        # Ad performance
        context['ad_performance'] = Advertisement.objects.filter(
            is_active=True
        ).order_by('-clicks')[:10]

        # Top viewed articles
        context['top_articles'] = News.objects.filter(
            is_published=True
        ).order_by('-views_count')[:10]

        # Calculate totals
        total_views = News.objects.aggregate(Sum('views_count'))['views_count__sum'] or 0
        total_clicks = Advertisement.objects.aggregate(Sum('clicks'))['clicks__sum'] or 0
        total_impressions = Advertisement.objects.aggregate(Sum('impressions'))['impressions__sum'] or 0

        context['total_views'] = total_views
        context['total_clicks'] = total_clicks
        context['total_impressions'] = total_impressions
        context['average_ctr'] = round((total_clicks / total_impressions * 100) if total_impressions > 0 else 0, 2)
        context['active_ads_count'] = Advertisement.objects.filter(is_active=True).count()

        return context


class NewsEditView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'custom_admin/news_edit.html'

    def get(self, request, news_id=None):
        if news_id:
            article = get_object_or_404(News, id=news_id)
        else:
            article = News()  # New article

        context = {
            'article': article,
            'categories': Category.objects.all(),
            'authors': Author.objects.all(),
        }
        return render(request, self.template_name, context)

    def post(self, request, news_id=None):
        if news_id:
            article = get_object_or_404(News, id=news_id)
        else:
            article = News()

        # Update article fields
        article.title = request.POST.get('title')
        article.slug = request.POST.get('slug') or slugify(article.title)
        article.description = request.POST.get('description')
        article.content = request.POST.get('content')

        # Handle category and author
        category_id = request.POST.get('category')
        if category_id:
            article.category = Category.objects.get(id=category_id)

        author_id = request.POST.get('author')
        if author_id:
            article.author = Author.objects.get(id=author_id)
        elif not article.author_id:
            # Default to first author if none selected
            article.author = Author.objects.first()

        # Handle boolean fields
        article.is_published = 'is_published' in request.POST
        article.is_featured = 'is_featured' in request.POST
        article.is_breaking = 'is_breaking' in request.POST
        article.is_trending = 'is_trending' in request.POST

        # Handle priority
        article.priority = request.POST.get('priority', 'normal')

        # Handle publish date
        publish_date = request.POST.get('publish_date')
        if publish_date:
            article.publish_date = timezone.datetime.fromisoformat(publish_date)

        # Handle image upload
        if 'image' in request.FILES:
            article.image = request.FILES['image']
        elif request.POST.get('thumbnail_url'):
            article.thumbnail_url = request.POST.get('thumbnail_url')

        article.save()

        # Handle tags
        tags_str = request.POST.get('tags', '')
        if tags_str:
            tag_names = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
            article.tags.clear()
            for tag_name in tag_names:
                article.tags.add(tag_name)

        messages.success(request, f'Article "{article.title}" saved successfully!')
        return redirect('custom_admin:news_edit', news_id=article.id)


class ContentManagementView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'custom_admin/content.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['all_news'] = News.objects.order_by('-timestamp')
        context['categories'] = Category.objects.all()
        context['authors'] = Author.objects.all()
        
        return context


class AdManagementView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'custom_admin/ads.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['advertisements'] = Advertisement.objects.all().order_by('-created_at')
        
        return context


class UserManagementView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'custom_admin/users.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['users'] = User.objects.all().order_by('-date_joined')
        context['newsletter_subscribers'] = Newsletter.objects.filter(is_active=True)
        
        return context


class SettingsView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'custom_admin/settings.html'


class NewsAPIManagementView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'custom_admin/news_api.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'NewsData.io API Management'

        # Get API configuration status
        from django.conf import settings
        context['api_configured'] = bool(getattr(settings, 'NEWSDATA_API_KEY', ''))
        context['api_base_url'] = getattr(settings, 'NEWSDATA_BASE_URL', '')
        context['default_categories'] = getattr(settings, 'DEFAULT_NEWS_CATEGORIES', [])

        return context


@user_passes_test(lambda u: u.is_staff)
def get_dashboard_stats(request):
    """AJAX endpoint for dashboard statistics"""
    stats = {
        'total_news': News.objects.count(),
        'published_news': News.objects.filter(is_published=True).count(),
        'total_views': News.objects.aggregate(Sum('views_count'))['views_count__sum'] or 0,
        'total_comments': Comment.objects.count(),
        'active_ads': Advertisement.objects.filter(is_active=True).count(),
        'newsletter_subscribers': Newsletter.objects.filter(is_active=True).count(),
    }
    return JsonResponse(stats)


@require_POST
@user_passes_test(lambda u: u.is_staff)
def toggle_news_status(request, news_id):
    """Toggle news publication status"""
    news = get_object_or_404(News, id=news_id)
    news.is_published = not news.is_published
    news.save()
    
    return JsonResponse({
        'success': True,
        'is_published': news.is_published
    })


@require_POST
@user_passes_test(lambda u: u.is_staff)
def toggle_ad_status(request, ad_id):
    """Toggle advertisement active status"""
    ad = get_object_or_404(Advertisement, id=ad_id)
    ad.is_active = not ad.is_active
    ad.save()
    
    return JsonResponse({
        'success': True,
        'is_active': ad.is_active
    })
