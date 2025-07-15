from django import template
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from news.models import Advertisement
from django.utils import timezone
from django.db.models import Q

register = template.Library()

@register.inclusion_tag('site/includes/ad_display.html')
def display_ad(ad_type, ad_size=None, css_class=""):
    """Display an active advertisement of the specified type and size"""
    now = timezone.now()

    # Build query for active ads only
    query = Q(
        ad_type=ad_type,
        is_active=True,
        start_date__lte=now
    ) & (Q(end_date__isnull=True) | Q(end_date__gte=now))

    if ad_size:
        query &= Q(ad_size=ad_size)

    # Get the first matching ad
    ad = Advertisement.objects.filter(query).first()



    return {
        'ad': ad,
        'css_class': css_class,
        'ad_type': ad_type,
        'ad_size': ad_size
    }

@register.simple_tag
def get_ads(ad_type, limit=1):
    """Get active advertisements of specified type"""
    now = timezone.now()
    
    ads = Advertisement.objects.filter(
        ad_type=ad_type,
        is_active=True,
        start_date__lte=now
    ).filter(
        Q(end_date__isnull=True) | Q(end_date__gte=now)
    )[:limit]
    
    return ads

@register.simple_tag
def increment_ad_impressions(ad_id):
    """Increment ad impressions count"""
    try:
        ad = Advertisement.objects.get(id=ad_id)
        ad.impressions += 1
        ad.save(update_fields=['impressions'])
        return ""
    except Advertisement.DoesNotExist:
        return ""

@register.filter
def ad_image_url(ad):
    """Get the ad image URL with fallback"""
    if ad and ad.image:
        return ad.image.url
    return static('assets/img/category_advertisement.jpg')

@register.simple_tag
def ad_click_url(ad):
    """Generate ad click tracking URL"""
    if ad and ad.url:
        return f"/ad-click/{ad.id}/?url={ad.url}"
    return "#"

@register.simple_tag
def has_active_ads(ad_type, ad_size=None):
    """Check if there are any active ads for the specified type and size"""
    now = timezone.now()

    query = Q(
        ad_type=ad_type,
        is_active=True,
        start_date__lte=now
    ) & (Q(end_date__isnull=True) | Q(end_date__gte=now))

    if ad_size:
        query &= Q(ad_size=ad_size)

    return Advertisement.objects.filter(query).exists()
