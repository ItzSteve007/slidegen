
from django.shortcuts import render, redirect
from .models import UploadedImage
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.http import HttpResponse,FileResponse
from .generate_ppt import generate_ppt
from .classifier import classify_theme
from datetime import datetime
from .generate_ppt import generate_ppt
from .classifier import classify_theme



@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def upload_images(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        for img in images:
            UploadedImage.objects.create(image=img)
        return redirect('dashboard')

@login_required
def create_ppt(request):
    if request.method == 'POST':
        images = UploadedImage.objects.all()

        # Collect full paths of uploaded images
        image_paths = [os.path.join(settings.MEDIA_ROOT, str(img.image)) for img in images]

        # Run classifier to detect theme
        theme = classify_theme(image_paths)

        # Output path for the generated presentation
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"{theme}_presentation_{timestamp}.pptx"
        output_path = os.path.join(settings.MEDIA_ROOT, 'presentations', output_filename)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Generate PPT
        generate_ppt(theme, image_paths, output_path)

        # Serve download link
        download_url = settings.MEDIA_URL + f"presentations/{output_filename}"
        return render(request, 'dashboard.html', {'download_url': download_url})
