from django.db.models.signals import post_save, post_delete
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import LoginActivity, AuditLog, ProcessedImage

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    LoginActivity.objects.create(
        user=user,
        ip_address=ip,
        user_agent=user_agent
    )

# Simple audit logging for ProcessedImage
@receiver(post_save, sender=ProcessedImage)
def log_image_save(sender, instance, created, **kwargs):
    # This is a bit tricky since we don't have the user request here easily
    # We'll just log that it happened. For full "reason" tracking, we'd need
    # to handle this in the View or Form.
    # However, for now, we assume implicit creation.
    action = 'CREATE' if created else 'UPDATE'
    AuditLog.objects.create(
        user=instance.user,
        action=action,
        object_type='ProcessedImage',
        object_name=instance.original_name,
        change_reason="Auto-logged via signal"
    )

@receiver(post_delete, sender=ProcessedImage)
def log_image_delete(sender, instance, **kwargs):
    AuditLog.objects.create(
        user=instance.user,
        action='DELETE',
        object_type='ProcessedImage',
        object_name=instance.original_name,
        change_reason="Auto-logged via signal"
    )
