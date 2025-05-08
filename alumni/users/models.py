from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('alumni', 'Alumni'),
        ('coordinator', 'Alumni Coordinator'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    # Additional fields
    register_number = models.CharField(max_length=30, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    academic_year = models.CharField(max_length=10, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)



# user/models.py
from django.db import models

class ValidRegisterNumber(models.Model):
    register_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.register_number


