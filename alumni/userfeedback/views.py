from django.shortcuts import render, redirect
from .forms import FeedbackForm
from .models import Feedback
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Your feedback has been submitted.')
            return redirect('submit_feedback')
    else:
        form = FeedbackForm()
    return render(request, 'feedback/submit_feedback.html', {'form': form})

@login_required
def admin_view_feedback(request):
    if request.user.is_superuser:  # Only admin can access this
        feedbacks = Feedback.objects.all().order_by('-submitted_at')
        return render(request, 'feedback/view_feedback.html', {'feedbacks': feedbacks})
    else:
        return redirect('submit_feedback')
