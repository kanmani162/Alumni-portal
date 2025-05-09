
# gallery/admin.py
from django.contrib import admin
from .models import Media

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'video')
