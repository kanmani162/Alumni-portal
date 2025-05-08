from django.shortcuts import render
from .models import CollegePost

def college_posts(request):
    posts = CollegePost.objects.all()
    return render(request, 'college_posts.html', {'posts': posts})
