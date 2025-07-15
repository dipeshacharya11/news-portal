
from django.urls import path
from .views import *

app_name = "account"



urlpatterns = [
    
    path('login/', LogInView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('profile/<int:id>/', ProfileView.as_view(), name="profile"),
    path('profile/', ProfileView.as_view(), name="profile"),  # Add this for general profile access
    path('register/', RegisterView.as_view(), name="register"),
    path('settings/', SettingView.as_view() ,name="setting"),
    path('settings/', SettingView.as_view() ,name="settings"),  # Add this for settings
    path('profile/update/',EditProfileView ,name="profile-update"),
    path('password/', ChangePassword, name='change_password'),

    
 
    
]