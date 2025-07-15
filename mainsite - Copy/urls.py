
from django.urls import path
from .views import *


app_name = "newspaper"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('single/', SingleView.as_view(), name='single-page'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('post/<slug:slug>/', PostSingleView.as_view(), name='single-post'),
    path('tag/<slug:tag>/', FilterByTag, name='tag'),
    path('ad-click/<int:ad_id>/', AdClickView.as_view(), name='ad-click'),
    
    # Additional URL patterns for enhanced UI
    path('latest/', BlogView.as_view(), name='latest_news'),
    path('trending/', BlogView.as_view(), name='trending'),
    path('breaking/', BlogView.as_view(), name='breaking_news'),
    path('categories/', BlogView.as_view(), name='category_list'),
    path('about/', BlogView.as_view(), name='about'),
    path('contact/', BlogView.as_view(), name='contact'),
    path('privacy/', BlogView.as_view(), name='privacy'),
    path('terms/', BlogView.as_view(), name='terms'),
]
