from django.contrib import admin
from django.utils.html import format_html
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'timestamp')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_articles_count')
    search_fields = ('user__username', 'user__email')

    def get_articles_count(self, obj):
        return obj.author.count()
    get_articles_count.short_description = 'Articles Count'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_published', 'is_featured', 'is_breaking', 'priority', 'views_count', 'timestamp')
    list_filter = ('is_published', 'is_featured', 'is_breaking', 'priority', 'category', 'timestamp')
    search_fields = ('title', 'description', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published', 'is_featured', 'is_breaking', 'priority')
    readonly_fields = ('views_count', 'timestamp', 'updated_at')
    date_hierarchy = 'timestamp'

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Content', {
            'fields': ('description', 'content', 'thumbnail', 'thumbnail_url')
        }),
        ('Publishing', {
            'fields': ('is_published', 'publish_date', 'priority')
        }),
        ('Features', {
            'fields': ('is_featured', 'is_trending', 'is_breaking')
        }),
        ('Tags', {
            'fields': ('tags',)
        }),
        ('Statistics', {
            'fields': ('views_count', 'timestamp', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'ad_type', 'ad_size', 'is_active', 'clicks', 'impressions', 'ctr', 'start_date', 'end_date')
    list_filter = ('ad_type', 'ad_size', 'is_active', 'start_date')
    search_fields = ('title',)
    list_editable = ('is_active',)
    readonly_fields = ('clicks', 'impressions', 'created_at')

    def ctr(self, obj):
        if obj.impressions > 0:
            return f"{(obj.clicks / obj.impressions * 100):.2f}%"
        return "0%"
    ctr.short_description = 'CTR'

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'ad_type', 'ad_size')
        }),
        ('Content', {
            'fields': ('image', 'html_content', 'url')
        }),
        ('Schedule', {
            'fields': ('is_active', 'start_date', 'end_date')
        }),
        ('Statistics', {
            'fields': ('clicks', 'impressions', 'created_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BreakingNews)
class BreakingNewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'expires_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'content')
    list_editable = ('is_active',)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'subscribed_at')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    list_editable = ('is_active',)
