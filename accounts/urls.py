from django.urls import path
from . import views
app_name = 'accounts'  # This is crucial to define the namespace
urlpatterns = [
    path('login/', views.login_view, name='login'),  # Login page
    path('register/', views.register_view, name='register'),  # Register page
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('upload-profile-pic/', views.upload_profile_pic, name='upload_profile_pic'),
    path('profile/update/dietary/', views.update_dietary_preferences, name='update_dietary_preferences'),
    path('update-security-settings/', views.update_security_settings, name='update_security_settings'),
    path('help-support/', views.help_support, name='help_support'),
    path('feedback/', views.feedback, name='feedback'),
    path('logout/', views.logout_view, name='logout'),
]
