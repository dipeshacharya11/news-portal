from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import json
import random

from news.models import Advertisement


class AdView(View):
    """Base view for advertisement handling"""
    
    def get_active_ads(self, ad_type=None, ad_size=None):
        """Get active advertisements"""
        ads = Advertisement.objects.filter(is_active=True)
        
        if ad_type:
            ads = ads.filter(ad_type=ad_type)
        if ad_size:
            ads = ads.filter(ad_size=ad_size)
            
        # Filter by date range
        ads = [ad for ad in ads if ad.is_valid()]
        
        return ads


@api_view(['GET'])
@permission_classes([AllowAny])
def get_banner_ad(request):
    """Get banner advertisement"""
    ads = Advertisement.objects.filter(
        ad_type='banner',
        is_active=True
    )
    
    # Filter valid ads
    valid_ads = [ad for ad in ads if ad.is_valid()]
    
    if valid_ads:
        # Random selection for rotation
        ad = random.choice(valid_ads)
        
        # Track impression
        ad.increment_impressions()
        
        return Response({
            'success': True,
            'ad': {
                'id': ad.id,
                'title': ad.title,
                'image': ad.image.url if ad.image else None,
                'html_content': ad.html_content,
                'url': ad.url,
                'ad_size': ad.ad_size,
            }
        })
    
    return Response({'success': False, 'message': 'No ads available'})


@api_view(['GET'])
@permission_classes([AllowAny])
def get_sidebar_ad(request):
    """Get sidebar advertisement"""
    ads = Advertisement.objects.filter(
        ad_type='sidebar',
        is_active=True
    )
    
    valid_ads = [ad for ad in ads if ad.is_valid()]
    
    if valid_ads:
        ad = random.choice(valid_ads)
        ad.increment_impressions()
        
        return Response({
            'success': True,
            'ad': {
                'id': ad.id,
                'title': ad.title,
                'image': ad.image.url if ad.image else None,
                'html_content': ad.html_content,
                'url': ad.url,
                'ad_size': ad.ad_size,
            }
        })
    
    return Response({'success': False, 'message': 'No ads available'})


@api_view(['GET'])
@permission_classes([AllowAny])
def get_popup_ad(request):
    """Get popup advertisement"""
    ads = Advertisement.objects.filter(
        ad_type='popup',
        is_active=True
    )
    
    valid_ads = [ad for ad in ads if ad.is_valid()]
    
    if valid_ads:
        ad = random.choice(valid_ads)
        ad.increment_impressions()
        
        return Response({
            'success': True,
            'ad': {
                'id': ad.id,
                'title': ad.title,
                'image': ad.image.url if ad.image else None,
                'html_content': ad.html_content,
                'url': ad.url,
                'ad_size': ad.ad_size,
            }
        })
    
    return Response({'success': False, 'message': 'No ads available'})


@api_view(['GET'])
@permission_classes([AllowAny])
def get_inline_ad(request):
    """Get inline content advertisement"""
    ads = Advertisement.objects.filter(
        ad_type='inline',
        is_active=True
    )
    
    valid_ads = [ad for ad in ads if ad.is_valid()]
    
    if valid_ads:
        ad = random.choice(valid_ads)
        ad.increment_impressions()
        
        return Response({
            'success': True,
            'ad': {
                'id': ad.id,
                'title': ad.title,
                'image': ad.image.url if ad.image else None,
                'html_content': ad.html_content,
                'url': ad.url,
                'ad_size': ad.ad_size,
            }
        })
    
    return Response({'success': False, 'message': 'No ads available'})


@require_POST
@csrf_exempt
def track_ad_click(request, ad_id):
    """Track advertisement click"""
    try:
        ad = get_object_or_404(Advertisement, id=ad_id)
        ad.increment_clicks()
        
        return JsonResponse({
            'success': True,
            'message': 'Click tracked successfully'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@require_POST
@csrf_exempt
def track_ad_impression(request, ad_id):
    """Track advertisement impression"""
    try:
        ad = get_object_or_404(Advertisement, id=ad_id)
        ad.increment_impressions()
        
        return JsonResponse({
            'success': True,
            'message': 'Impression tracked successfully'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_ad_by_zone(request, zone):
    """Get advertisement by zone"""
    zone_mapping = {
        'header': 'header',
        'footer': 'footer',
        'sidebar': 'sidebar',
        'banner': 'banner',
        'popup': 'popup',
        'inline': 'inline',
    }
    
    ad_type = zone_mapping.get(zone)
    if not ad_type:
        return Response({'success': False, 'message': 'Invalid zone'}, status=400)
    
    ads = Advertisement.objects.filter(
        ad_type=ad_type,
        is_active=True
    )
    
    valid_ads = [ad for ad in ads if ad.is_valid()]
    
    if valid_ads:
        ad = random.choice(valid_ads)
        ad.increment_impressions()
        
        return Response({
            'success': True,
            'ad': {
                'id': ad.id,
                'title': ad.title,
                'image': ad.image.url if ad.image else None,
                'html_content': ad.html_content,
                'url': ad.url,
                'ad_size': ad.ad_size,
                'ad_type': ad.ad_type,
            }
        })
    
    return Response({'success': False, 'message': 'No ads available for this zone'})


@api_view(['GET'])
@permission_classes([AllowAny])
def get_ad_stats(request):
    """Get advertisement statistics"""
    if not request.user.is_staff:
        return Response({'error': 'Permission denied'}, status=403)
    
    ads = Advertisement.objects.filter(is_active=True)
    
    stats = []
    for ad in ads:
        ctr = (ad.clicks / ad.impressions * 100) if ad.impressions > 0 else 0
        stats.append({
            'id': ad.id,
            'title': ad.title,
            'ad_type': ad.ad_type,
            'clicks': ad.clicks,
            'impressions': ad.impressions,
            'ctr': round(ctr, 2),
            'is_valid': ad.is_valid(),
        })
    
    return Response({
        'success': True,
        'stats': stats,
        'total_ads': len(ads),
        'total_clicks': sum(ad.clicks for ad in ads),
        'total_impressions': sum(ad.impressions for ad in ads),
    })
