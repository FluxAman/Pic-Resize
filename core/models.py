from django.db import models
from django.contrib.auth.models import User

class ProcessedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='processed_images')
    image = models.ImageField(upload_to='processed/')
    original_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Store settings used? Maybe later.
    
    def __str__(self):
        return f"{self.original_name} - {self.user.username}"
