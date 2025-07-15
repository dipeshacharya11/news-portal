from taggit.managers import TaggableManager
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

User = settings.AUTH_USER_MODEL


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(
        upload_to='profile_pic/%Y-%m-%d/', blank=True, null=True)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        db_table = "authors"

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)
    parent = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.CASCADE, related_name='children')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("newspaper:category", kwargs={'slug': self.slug})


class News(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('breaking', 'Breaking News'),
    ]

    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='author')
    title = models.CharField(max_length=250, blank=False)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)
    description = models.TextField()
    content = models.TextField(help_text="Full article content", default="", blank=True)
    thumbnail = models.ImageField(upload_to='photos/news/%Y-%m-%d/', blank=True, null=True)
    thumbnail_url = models.URLField(max_length=300, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(default=timezone.now)
    # ratings = GenericRelation(Rating, related_query_name='ratings')
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False, help_text="Show on homepage featured section")
    is_trending = models.BooleanField(default=False, help_text="Mark as trending news")
    is_breaking = models.BooleanField(default=False, help_text="Breaking news alert")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    views_count = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category')
    tags = TaggableManager()

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        db_table = "news"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("newspaper:single-post", kwargs={'slug': self.slug})

    # @property
    def get_comment_count(self):
        # comment_count = News.objects.all().annotate(Count('post__id')).order_by('-post__id__count')
        comment_count = self.post.values(
            'post__id').aggregate(models.Count('post__id'))
        return comment_count['post__id__count']

    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])

    @property
    def reading_time(self):
        """Calculate estimated reading time"""
        word_count = len(self.content.split()) if self.content else len(self.description.split())
        return max(1, word_count // 200)  # Assuming 200 words per minute


class Advertisement(models.Model):
    AD_TYPES = [
        ('banner', 'Banner'),
        ('sidebar', 'Sidebar'),
        ('popup', 'Popup'),
        ('inline', 'Inline Content'),
        ('header', 'Header'),
        ('footer', 'Footer'),
    ]

    AD_SIZES = [
        ('728x90', 'Leaderboard (728x90)'),
        ('300x250', 'Medium Rectangle (300x250)'),
        ('320x50', 'Mobile Banner (320x50)'),
        ('160x600', 'Wide Skyscraper (160x600)'),
        ('300x600', 'Half Page (300x600)'),
        ('970x250', 'Billboard (970x250)'),
    ]

    title = models.CharField(max_length=200)
    ad_type = models.CharField(max_length=20, choices=AD_TYPES)
    ad_size = models.CharField(max_length=20, choices=AD_SIZES)
    image = models.ImageField(upload_to='ads/%Y-%m-%d/', blank=True, null=True)
    html_content = models.TextField(blank=True, help_text="Custom HTML/JavaScript code")
    url = models.URLField(blank=True, help_text="Click destination URL")
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)
    clicks = models.PositiveIntegerField(default=0)
    impressions = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Advertisement"
        verbose_name_plural = "Advertisements"
        db_table = "advertisements"

    def __str__(self):
        return f"{self.title} ({self.ad_type})"

    def is_valid(self):
        """Check if ad is currently valid"""
        now = timezone.now()
        if self.end_date:
            return self.is_active and self.start_date <= now <= self.end_date
        return self.is_active and self.start_date <= now

    def increment_clicks(self):
        """Increment click count"""
        self.clicks += 1
        self.save(update_fields=['clicks'])

    def increment_impressions(self):
        """Increment impression count"""
        self.impressions += 1
        self.save(update_fields=['impressions'])


class BreakingNews(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Breaking News"
        verbose_name_plural = "Breaking News"
        db_table = "breaking_news"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_valid(self):
        """Check if breaking news is still valid"""
        now = timezone.now()
        if self.expires_at:
            return self.is_active and now <= self.expires_at
        return self.is_active


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"
        db_table = "newsletter_subscriptions"

    def __str__(self):
        return self.email
