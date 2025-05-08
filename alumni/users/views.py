from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserForm
from .models import ValidRegisterNumber
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST, request.FILES)
        if form.is_valid():
            register_number = form.cleaned_data['register_number']
            user_type = form.cleaned_data['user_type']

            # Check if register number is authorized
            if not ValidRegisterNumber.objects.filter(register_number=register_number).exists():
                return render(request, 'users/register.html', {
                    'form': form,
                    'error': 'This register number is not authorized.'
                })

            if user_type not in ['student', 'alumni', 'admin']:
                return render(request, 'users/register.html', {
                    'form': form,
                    'error': 'Only students, alumni, or admins can register.'
                })

            user = form.save()
            login(request, user)

            # Optional: remove used register number (to avoid reuse)
            # ValidRegisterNumber.objects.filter(register_number=register_number).delete()

            return redirect('dashboard')
    else:
        form = CustomUserForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            if user.user_type not in ['student', 'alumni', 'admin']:
                return render(request, 'users/login.html', {'error': 'Access denied: invalid user type.'})
            
            if not ValidRegisterNumber.objects.filter(register_number=user.register_number).exists():
                return render(request, 'users/login.html', {'error': 'Access denied: unauthorized register number.'})

            login(request, user)
            return redirect('dashboard')

        return render(request, 'users/login.html', {'error': 'Invalid credentials.'})

    return render(request, 'users/login.html')


@login_required
def dashboard(request):
    # Ensure logged-in user's register_number is still valid
    if not ValidRegisterNumber.objects.filter(register_number=request.user.register_number).exists():
        logout(request)
        return redirect('login')

    return render(request, 'dashboard.html')


def user_logout(request):
    logout(request)
    return redirect('login')




from django.shortcuts import render
from jobs.models import JobPost
from college_posts.models import CollegePost
from users.models import CustomUser

def admin_dashboard(request):
    if request.user.user_type != 'admin':
        return redirect('dashboard')

    job_count = JobPost.objects.count()
    college_posts = CollegePost.objects.count()
    user_count = CustomUser.objects.count()

    context = {
        'job_count': job_count,
        'college_posts': college_posts,
        'user_count': user_count,
    }
    return render(request, 'users/admin_dashboard.html', context)

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        user.username = request.POST.get("username")
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.register_number = request.POST.get("register_number")
        user.department = request.POST.get("department")
        user.academic_year = request.POST.get("academic_year")
        user.phone_number = request.POST.get("phone_number")
        user.address = request.POST.get("address")

        password = request.POST.get("password")
        if password:
            user.set_password(password)  # securely update password

        user.save()
        login(request, user)  # Re-authenticate if password was changed
        return redirect('profile')
    
    return render(request, 'users/edit_profile.html', {'user': user})


@login_required
def chat(request):
    if request.method == "POST":
        message = request.POST['message']
        if 'chat_messages' not in request.session:
            request.session['chat_messages'] = []
        request.session['chat_messages'].append({
            'username': request.user.username,
            'message': message
        })
        request.session.modified = True
        return redirect('chat')  # Redirect to refresh the chat with new message

    return render(request, 'users/chat.html', {
        'chat_messages': request.session.get('chat_messages', [])
    })


import io
import datetime
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from matplotlib import pyplot as plt
from users.models import CustomUser
from collections import Counter

def generate_user_report(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Header Section
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width / 2, height - 50, "User Report")
    
    p.setFont("Helvetica", 12)
    p.setFillColor(colors.gray)
    p.drawCentredString(width / 2, height - 70, f"Generated on: {datetime.datetime.now().strftime('%d %B %Y, %H:%M')}")

    p.setFillColor(colors.black)
    y = height - 100

    # Table Header
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Username")
    p.drawString(200, y, "Email")
    p.drawString(400, y, "User Type")

    y -= 15
    p.line(50, y, width - 50, y)  # underline

    # Table Data
    p.setFont("Helvetica", 11)
    y -= 20
    users = CustomUser.objects.all()
    for user in users:
        p.drawString(50, y, user.username)
        p.drawString(200, y, user.email[:30])  # truncate long emails
        p.drawString(400, y, user.user_type)
        y -= 18

        if y < 100:
            p.showPage()
            y = height - 50

    # Chart Section
    user_type_counts = Counter([u.user_type for u in users])
    labels = list(user_type_counts.keys())
    values = list(user_type_counts.values())

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, shadow=True)
    ax.set_title('User Type Distribution', fontsize=14)

    chart_buf = io.BytesIO()
    plt.savefig(chart_buf, format='png', bbox_inches='tight')
    plt.close(fig)
    chart_buf.seek(0)

    # Add new page for chart
    p.showPage()
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 80, "User Type Distribution")

    p.drawImage(ImageReader(chart_buf), 100, 200, width=400, height=400)

    # Footer
    p.setFont("Helvetica", 10)
    p.drawCentredString(width / 2, 50, f"Total Users: {len(users)}")

    # Finalize PDF
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='user_report.pdf')

from django.shortcuts import render

def dashboard_view(request):
    image_list = [
        'images/images (1).jpg'        
        'images/images (2).jpg',
        'images/images.jpg',
    ]
    return render(request, 'index.html', {'image_list': image_list})

