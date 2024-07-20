# models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    fixed_income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    variable_income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    insurance = models.CharField(max_length=100, blank=True, null=True)
    savings = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    expenses = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}'

class UploadedFile(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'{self.user_profile.user.username} - {self.file.name}'