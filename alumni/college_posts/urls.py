from django.urls import path
from . import views

urlpatterns = [
    path('', views.college_posts, name='college_posts'),
]

