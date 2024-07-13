# forms.py

from django import forms
from django.contrib.auth.forms import PasswordResetForm

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
