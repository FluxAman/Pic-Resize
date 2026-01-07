from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import ProcessedImage
from datetime import timedelta

class Command(BaseCommand):
    help = 'Deletes processed images older than 24 hours'

    def handle(self, *args, **options):
        cutoff_time = timezone.now() - timedelta(hours=24)
        old_images = ProcessedImage.objects.filter(created_at__lt=cutoff_time)
        count = old_images.count()
        
        for img in old_images:
            img.image.delete(save=False) # Delete actual file
            img.delete() # Delete DB record
            
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} old images'))
