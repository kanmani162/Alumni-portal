from django.contrib import admin
from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'submitted_at', 'message')
    list_filter = ('submitted_at',)
    search_fields = ('user__username', 'message')

admin.site.register(Feedback, FeedbackAdmin)
