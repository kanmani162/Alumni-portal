from django.contrib import admin
from .models import CollegePost

class CollegePostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)

admin.site.register(CollegePost, CollegePostAdmin)
