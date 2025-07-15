
from django.urls import path, include
from .views import NewsApiView, SingleNewsApiView
from .ad_views import (
    get_banner_ad, get_sidebar_ad, get_popup_ad, get_inline_ad,
    track_ad_click, track_ad_impression, get_ad_by_zone, get_ad_stats
)


urlpatterns = [
    path('news/', NewsApiView.as_view()),
    path('news/<slug:slug>/', SingleNewsApiView.as_view()),

    # Advertisement API endpoints
    path('ads/banner/', get_banner_ad, name='api_banner_ad'),
    path('ads/sidebar/', get_sidebar_ad, name='api_sidebar_ad'),
    path('ads/popup/', get_popup_ad, name='api_popup_ad'),
    path('ads/inline/', get_inline_ad, name='api_inline_ad'),
    path('ads/zone/<str:zone>/', get_ad_by_zone, name='api_ad_by_zone'),
    path('ads/click/<int:ad_id>/', track_ad_click, name='api_track_click'),
    path('ads/impression/<int:ad_id>/', track_ad_impression, name='api_track_impression'),
    path('ads/stats/', get_ad_stats, name='api_ad_stats'),
]
