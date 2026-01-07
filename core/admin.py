from django.contrib import admin
from .models import ProcessedImage, LoginActivity, AuditLog

@admin.register(ProcessedImage)
class ProcessedImageAdmin(admin.ModelAdmin):
    list_display = ('original_name', 'user', 'created_at')
    search_fields = ('original_name', 'user__username')
    list_filter = ('created_at',)

@admin.register(LoginActivity)
class LoginActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'timestamp')
    search_fields = ('user__username', 'ip_address')
    list_filter = ('timestamp',)
    readonly_fields = ('user', 'ip_address', 'user_agent', 'timestamp')

    def has_add_permission(self, request):
        return False

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'object_type', 'object_name', 'timestamp')
    search_fields = ('user__username', 'object_name', 'change_reason')
    list_filter = ('action', 'timestamp')
    readonly_fields = ('user', 'action', 'object_type', 'object_name', 'change_reason', 'timestamp')

    def has_add_permission(self, request):
        return False
