from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    attendance_count = models.IntegerField(default=0)
    matric_number = models.CharField(max_length=15, unique=True, null=True, blank=True)  # ✅ Allow existing users without Matric Numbers
    first_name = models.CharField(max_length=50)  # ✅ First Name
    last_name = models.CharField(max_length=50)  # ✅ Last Name
    def clean_matric_number(self):
        """Ensure Matric Number is unique before saving"""
        matric_number = self.cleaned_data.get('matric_number')
        if User.objects.filter(matric_number=matric_number).exists():
            raise ValidationError("❌ This Matric Number is already registered.")
        return matric_number
    
    
    def __str__(self):
        return f"{self.matric_number} - {self.username}" if self.matric_number else self.username

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class AttendanceControl(models.Model):
    """Model to store attendance status (open or closed)."""
    is_open = models.BooleanField(default=True)  # ✅ Default: Attendance is open
    last_updated = models.DateTimeField(auto_now=True)  # ✅ Timestamp of last change
    allowed_latitude = models.FloatField(default=0.0)  # ✅ Latitude of allowed location
    allowed_longitude = models.FloatField(default=0.0)  # ✅ Longitude of allowed location
    radius_meters = models.FloatField(default=100) 

    def __str__(self):
        return "Open" if self.is_open else "Closed"