from django.contrib import admin
from .models import Credentials, SecureNote, ActivityLog

@admin.register(Credentials)
class CredentialsAdmin(admin.ModelAdmin):
    list_display = ('label', 'type', 'user', 'username', 'email', 'is_favorite', 'created_at', 'updated_at')
    list_filter = ('type', 'is_favorite', 'created_at', 'user')
    search_fields = ('label', 'username', 'email', 'tags')
    readonly_fields = ('password_encrypted', 'secret_key_encrypted', 'created_at', 'updated_at', 'last_accessed')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'label', 'type', 'website_url', 'is_favorite')
        }),
        ('Login Credentials', {
            'fields': ('username', 'email', 'password_encrypted', 'secret_key_encrypted')
        }),
        ('Additional Information', {
            'fields': ('note', 'tags')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_accessed'),
            'classes': ('collapse',)
        }),
    )

@admin.register(SecureNote)
class SecureNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'user', 'is_favorite', 'created_at', 'updated_at')
    list_filter = ('type', 'is_favorite', 'created_at', 'user')
    search_fields = ('title', 'tags')
    readonly_fields = ('content_encrypted', 'created_at', 'updated_at', 'last_accessed')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'title', 'type', 'is_favorite')
        }),
        ('Content', {
            'fields': ('content_encrypted',)
        }),
        ('Additional Information', {
            'fields': ('tags',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_accessed'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'description', 'ip_address', 'timestamp')
    list_filter = ('action', 'timestamp', 'user')
    search_fields = ('user__username', 'description', 'ip_address')
    readonly_fields = ('user', 'action', 'description', 'ip_address', 'user_agent', 'timestamp')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
