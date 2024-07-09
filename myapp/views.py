from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
import json

# Replace with your actual client ID
GOOGLE_CLIENT_ID = '361382531750-m65ekgq6bhlo654o4d1mpbnjuf6vlnqq.apps.googleusercontent.com'


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('retype-password')
        if User.objects.filter(username=email).exists() :
            return render(request, 'signup.html', {'error': 'Email already exists'})
        if password != password1:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        user = User.objects.create_user(username=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'signup.html')

@csrf_exempt
def google_sign_in(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data.get('token')
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
            email = idinfo['email']
            user, created = User.objects.get_or_create(username=email)
            if created:
                user.set_unusable_password()
                user.save()
            login(request, user)
            return JsonResponse({'status': 'success'})

        except ValueError as e:
            return JsonResponse({'status': 'failure', 'message': str(e)})
    return JsonResponse({'status': 'failure', 'message': 'Invalid request method'})
@login_required
def home_view(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def password_reset_view(request):
    # Implement password reset logic here
    pass
