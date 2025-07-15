from django.shortcuts import render,  HttpResponseRedirect, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, View
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.http import JsonResponse

from mainsite.models import HomePageSettings
from news.models import Category, News, BreakingNews, Advertisement
from comment.models import Comment
from django.utils import timezone
from comment.form import CommentModelForm

from taggit.models import Tag


class HomeView(TemplateView):
    template_name = 'site/pages/index.html'

    def get_home_page_post_list(self):
        home_page_settings = HomePageSettings.objects.last()
        news_list = News.objects.filter(is_published=True)

        # Handle case when no homepage settings exist
        if not home_page_settings:
            # Create default homepage settings or use fallback logic
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
            trending = latest_news[1] if len(latest_news) > 1 else None
            editor_choice = latest_news[2] if len(latest_news) > 2 else None

            return (hot_news, post_catalog_one, post_catalog_two, post_catalog_three,
                    post_catalog_four, post_catalog_five, trending, editor_choice)

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

        return (home_page_settings.hot_news, post_catalog_one, post_catalog_two, post_catalog_three,
                post_catalog_four, post_catalog_five, home_page_settings.trending, home_page_settings.editor_choice)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results = self.get_home_page_post_list()
        context['hot_news'] = results[0]
        context['post_catalog_one'] = results[1]
        context['post_catalog_two'] = results[2]
        context['post_catalog_three'] = results[3]
        context['post_catalog_four'] = results[4]
        context['post_catalog_five'] = results[5]
        context['trending'] = results[6]
        context['editor_choice'] = results[7]

        # Enhanced news hierarchy and categorization
        context['categories'] = Category.objects.all()
        context['breaking_news'] = BreakingNews.objects.filter(is_active=True)[:3]

        # Priority-based news hierarchy
        context['breaking_news_items'] = News.objects.filter(
            is_published=True,
            is_breaking=True
        ).order_by('-timestamp')[:5]

        context['top_stories'] = News.objects.filter(
            is_published=True,
            priority='high'
        ).exclude(is_breaking=True).order_by('-timestamp')[:8]

        context['featured_news'] = News.objects.filter(
            is_published=True,
            is_featured=True
        ).exclude(is_breaking=True).order_by('-timestamp')[:6]

        context['trending_news'] = News.objects.filter(
            is_published=True,
            is_trending=True
        ).order_by('-views_count', '-timestamp')[:8]

        # Latest news with better categorization
        context['latest_news'] = News.objects.filter(
            is_published=True
        ).order_by('-timestamp')[:15]

        # Recent updates (last 24 hours)
        from datetime import timedelta
        yesterday = timezone.now() - timedelta(days=1)
        context['recent_updates'] = News.objects.filter(
            is_published=True,
            timestamp__gte=yesterday
        ).order_by('-timestamp')[:10]

        # Most viewed this week
        week_ago = timezone.now() - timedelta(days=7)
        context['most_viewed_week'] = News.objects.filter(
            is_published=True,
            timestamp__gte=week_ago
        ).order_by('-views_count')[:5]

        # Category-wise latest with better organization
        context['latest_by_category'] = {}
        all_categories = Category.objects.all()

        for category in all_categories:
            category_news = News.objects.filter(
                is_published=True,
                category=category
            ).order_by('-timestamp')[:6]

            if category_news.exists():
                context['latest_by_category'][category.name] = {
                    'category': category,
                    'news': category_news,
                    'count': News.objects.filter(is_published=True, category=category).count()
                }

        # Enhanced context for better frontend display
        context['total_news_count'] = News.objects.filter(is_published=True).count()
        context['total_categories'] = all_categories.count()

        # Today's news
        from datetime import date
        today = timezone.now().date()
        context['todays_news'] = News.objects.filter(
            is_published=True,
            timestamp__date=today
        ).order_by('-timestamp')[:10]

        # This week's most popular (by views if available, otherwise by recency)
        week_ago = timezone.now() - timedelta(days=7)
        context['weekly_popular'] = News.objects.filter(
            is_published=True,
            timestamp__gte=week_ago
        ).order_by('-timestamp')[:8]  # Since we don't have views_count field

        # API-sourced news (from NewsData.io)
        context['api_news'] = News.objects.filter(
            is_published=True,
            author__user__username='newsdata_api'
        ).order_by('-timestamp')[:12]

        # Add advertisements context
        now = timezone.now()
        context['header_ads'] = Advertisement.objects.filter(
            ad_type='header',
            is_active=True,
            start_date__lte=now
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=now)
        )[:1]

        context['banner_ads'] = Advertisement.objects.filter(
            ad_type='banner',
            is_active=True,
            start_date__lte=now
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=now)
        )[:2]

        context['sidebar_ads'] = Advertisement.objects.filter(
            ad_type='sidebar',
            is_active=True,
            start_date__lte=now
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=now)
        )[:3]

        context['footer_ads'] = Advertisement.objects.filter(
            ad_type='footer',
            is_active=True,
            start_date__lte=now
        ).filter(
            Q(end_date__isnull=True) | Q(end_date__gte=now)
        )[:1]

        return context


class SingleView(TemplateView):
    template_name = 'site/pages/single.html'


class BlogView(TemplateView):
    template_name = 'site/pages/blog.html'


# MultipleObjectMixin for adding paginate..
class CategoryView(DetailView, MultipleObjectMixin):
    model = Category  # Functionality for news
    paginate_by = 6
    context_object_name = 'category'
    template_name = 'site/pages/category.html'

    def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        news_list = News.objects.filter(
            category=self.object.id, is_published=True).order_by('-id')
        context = super().get_context_data(object_list=news_list, **kwargs)
        return context


class PostSingleView(DetailView, FormMixin):
    model = News
    context_object_name = 'news'
    form_class = CommentModelForm
    success_url = reverse_lazy('newspaper:blog')
    template_name = 'site/pages/single.html'

    def get_related_post_by_category(self):
        return super().get_queryset().filter(is_published='True', category=self.object.category.id).exclude(id=self.object.id).order_by('-id')

    # def get_related_post_filter_by_tag(self):
    #     for tag in Tag.objects.all():
    #         return self.get_related_post_by_category().filter(tags__name__in=[tag])[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = self.get_related_post_by_category()
        context['comments'] = Comment.objects.filter(
            post=self.object.id, reply=None)
        print('dd', context['related_posts'])
        return context

    def get_success_url(self):
        return reverse_lazy('newspaper:single-post', kwargs={'slug': self.kwargs['slug']})

    def post(self, request, *args, **kwargs):
        """Check Operation If the form is valid or invalid."""
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, comment_form):
        """If the form is valid, start save operation."""
        form = comment_form.save(commit=False)
        if self.request.user:
            form.user = self.request.user
        else:
            form.user = None
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return HttpResponseRedirect(self.get_success_url())


def FilterByTag(request, tag):
    news_list = News.objects.filter(
        tags__name__in=[tag], is_published=True).order_by('-id')
    context = {
        'news_list': news_list,
        'tag': tag
    }
    return render(request, 'site/pages/tag.html', context)


class AdClickView(View):
    """Handle advertisement click tracking"""

    def get(self, request, ad_id):
        """Handle GET request for ad click (redirect)"""
        ad = get_object_or_404(Advertisement, id=ad_id)

        # Increment click count
        ad.clicks += 1
        ad.save(update_fields=['clicks'])

        # Redirect to the ad URL
        if ad.url:
            return redirect(ad.url)
        else:
            return redirect('newspaper:home')

    def post(self, request, ad_id):
        """Handle POST request for ad click tracking (AJAX)"""
        ad = get_object_or_404(Advertisement, id=ad_id)

        # Increment click count
        ad.clicks += 1
        ad.save(update_fields=['clicks'])

        return JsonResponse({
            'success': True,
            'clicks': ad.clicks
        })
