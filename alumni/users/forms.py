from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username',
            'email',
            'phone_number',
            'register_number',
            'department',
            'academic_year',
            'address',
            'password1',
            'password2',
            'user_type'
            ]


