from django.urls import path
from . import views
from .views import generate_user_report

urlpatterns = [
     path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('chat/', views.chat, name='chat'),
    path('download/user-report/', generate_user_report, name='user_report_pdf'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
   
]


