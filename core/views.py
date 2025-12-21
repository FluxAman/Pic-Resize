import base64
import uuid
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.files.base import ContentFile
from .models import ProcessedImage

def index(request):
    return render(request, 'core/index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def save_image(request):
    if request.method == 'POST':
        # Expecting 'image' (blob/file) and 'filename'
        image_file = request.FILES.get('image')
        filename = request.POST.get('filename', 'processed_image.png')
        
        if not image_file:
            return JsonResponse({'error': 'No image provided'}, status=400)
            
        ProcessedImage.objects.create(
            user=request.user,
            image=image_file,
            original_name=filename
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request'}, status=405)

@login_required
def profile(request):
    images = request.user.processed_images.order_by('-created_at')
    return render(request, 'core/profile.html', {'images': images})
