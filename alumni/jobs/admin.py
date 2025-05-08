from django.contrib import admin
from .models import JobPost, JobApplication

class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'posted_by')
    search_fields = ('title', 'company', 'location')

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'student', 'status')
    list_filter = ('status',)

admin.site.register(JobPost, JobPostAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
