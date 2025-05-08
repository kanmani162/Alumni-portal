# gallery/views.py
from django.shortcuts import render
from .models import Media

def gallery_view(request):
    media_list = Media.objects.all()
    return render(request, 'gallery/gallery.html', {'media_list': media_list})
