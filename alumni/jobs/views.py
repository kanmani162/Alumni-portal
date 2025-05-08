from django.shortcuts import render, redirect
from .models import JobPost
from django.contrib.auth.decorators import login_required

@login_required
def job_list(request):
    jobs = JobPost.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

@login_required
def post_job(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        company = request.POST['company']
        location = request.POST['location']
        job = JobPost(title=title, description=description, company=company, location=location, posted_by=request.user)
        job.save()
        return redirect('job_list')
    return render(request, 'jobs/post_job.html')


from django.shortcuts import render, redirect
from .models import JobPost, JobApplication
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

@login_required
def apply_job(request, job_id):
    job = JobPost.objects.get(id=job_id)
    
    if request.method == "POST":
        resume = request.FILES['resume']
        fs = FileSystemStorage()
        file_path = fs.save(resume.name, resume)
        application = JobApplication(job=job, student=request.user, resume=file_path)
        application.save()
        return redirect('job_list')

    return render(request, 'jobs/apply_job.html', {'job': job})


from django.shortcuts import render, get_object_or_404, redirect
from .models import JobPost, JobApplication
from django.contrib.auth.decorators import login_required

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    
    # Check if the user already applied
    existing_application = JobApplication.objects.filter(job=job, student=request.user).exists()
    if not existing_application:
        JobApplication.objects.create(job=job, student=request.user)
    
    return redirect('job_list') 


