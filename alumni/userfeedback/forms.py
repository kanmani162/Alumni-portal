from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'placeholder': 'Enter your feedback here...',
                'class': 'form-control',
                'rows': 5
            }),
        }
