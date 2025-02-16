from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import User

def validate_image_format(image):
    """Ensure profile picture is JPG or PNG."""
    if not image.name.endswith(('.jpg', '.jpeg', '.png')):
        raise ValidationError('Only JPG and PNG images are allowed.')

class SignUpForm(UserCreationForm):
    """Signup Form with Matric Number, First Name, Last Name, and Profile Picture"""
    matric_number = forms.CharField(max_length=15, required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    profile_picture = forms.ImageField(required=True, validators=[validate_image_format])

    class Meta:
        model = User
        fields = ['username', 'matric_number', 'first_name', 'last_name', 'password1', 'password2', 'profile_picture']
