from django.urls import path
from . import views

app_name = 'backend'

urlpatterns = [
    # API endpoints
    path('stats/', views.api_user_stats, name='api_user_stats'),
    path('search/', views.api_search, name='api_search'),
    path('toggle-favorite/', views.api_toggle_favorite, name='api_toggle_favorite'),
] 