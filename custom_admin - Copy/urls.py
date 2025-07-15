from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    path('content/', views.ContentManagementView.as_view(), name='content'),
    path('ads/', views.AdManagementView.as_view(), name='ads'),
    path('news-api/', views.NewsAPIManagementView.as_view(), name='news_api'),
    path('users/', views.UserManagementView.as_view(), name='users'),
    path('settings/', views.SettingsView.as_view(), name='settings'),

    # Content editing
    path('news/add/', views.NewsEditView.as_view(), name='news_add'),
    path('news/<int:news_id>/edit/', views.NewsEditView.as_view(), name='news_edit'),

    # AJAX endpoints
    path('api/stats/', views.get_dashboard_stats, name='api_stats'),
    path('api/toggle-news/<int:news_id>/', views.toggle_news_status, name='toggle_news'),
    path('api/toggle-ad/<int:ad_id>/', views.toggle_ad_status, name='toggle_ad'),
]
