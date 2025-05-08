from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('<int:job_id>/apply/', views.apply_job, name='apply')
]

