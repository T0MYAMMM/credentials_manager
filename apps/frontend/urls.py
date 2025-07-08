from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    # Main dashboard
    path('', views.dashboard, name='dashboard'),
    # Add home alias for backward compatibility with tests
    path('home/', views.dashboard, name='home'),
    
    # Credentials management
    path('credentials/', views.credentials_list, name='credentials_list'),
    path('credentials/add/', views.credential_create, name='credential_create'),
    path('credentials/<int:pk>/', views.credential_detail, name='credential_detail'),
    path('credentials/<int:pk>/edit/', views.credential_edit, name='credential_edit'),
    path('credentials/<int:pk>/delete/', views.credential_delete, name='credential_delete'),
    
    # Notes management
    path('notes/', views.notes_list, name='notes_list'),
    path('notes/add/', views.note_create, name='note_create'),
    path('notes/<int:pk>/', views.note_detail, name='note_detail'),
    path('notes/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('notes/<int:pk>/delete/', views.note_delete, name='note_delete'),
    
    # Utility pages
    path('search/', views.search, name='search'),
    path('activity/', views.activity_log, name='activity_log'),
    
    # AJAX endpoints
    path('toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    
    # Data export
    path('export/', views.export_data, name='export_data'),
] 