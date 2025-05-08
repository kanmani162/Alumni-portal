from django.urls import path
from . import views

urlpatterns = [
    path('feedback/', views.submit_feedback, name='submit_feedback'),
    path('admin-feedback/', views.admin_view_feedback, name='admin_view_feedback'),
]
