from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
import json
from django.core.files.base import ContentFile
from django.db import IntegrityError
import yfinance as yf
from myapp.models import Companies
from django.contrib import messages
from lstm.RunModel import RunModel
from datetime import date, timedelta
from GoogleNews import GoogleNews

# Replace with your actual client ID
GOOGLE_CLIENT_ID = '361382531750-m65ekgq6bhlo654o4d1mpbnjuf6vlnqq.apps.googleusercontent.com'


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            print(f"User {user.username} logged in with session key: {request.session.session_key}")
            request.session.modified = True
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    else:
        return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('retype-password')
        
        if User.objects.filter(username=email).exists():
            return render(request, 'signup.html', {'error': 'Email already exists'})
        
        if password != password1:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        
        user = User.objects.create_user(username=email, password=password)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Explicitly specify the authentication backend
        return redirect('home')
    
    return render(request, 'signup.html')

@login_required
def save_google_profile_image(user_profile, image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        img_name = f'{user_profile.user.username}_google_profile.jpg'
        user_profile.image.save(img_name, ContentFile(response.content), save=True)


@csrf_exempt
def google_sign_in(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data.get('token')
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
            email = idinfo['email']
            
            # Check if the user already exists
            user, created = User.objects.get_or_create(username=email)
            
            if created:
                user.set_unusable_password()
                user.save()
            
            login(request, user)  # Login the user after creation or retrieval
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            
            # Set Google profile image if available
            if created and 'picture' in idinfo:
                save_google_profile_image(user_profile, idinfo['picture'])
            return JsonResponse({'status': 'success'})

        except ValueError as e:
            return JsonResponse({'status': 'failure', 'message': str(e)})
    
    return JsonResponse({'status': 'failure', 'message': 'Invalid request method'})
@login_required
def home_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    return render(request, 'home.html', {'profile': profile, 'user': request.user })

def dashboard_before_login(request):
    return render(request, 'dashboard_before_login.html')

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def form_page(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        dob = request.POST.get('dob')
        mobile = request.POST.get('mobile')
        fixed_income = request.POST.get('fixed-income')
        variable_income = request.POST.get('variable-income')
        profession = request.POST.get('profession')
        insurance = request.POST.get('insurance')
        savings = request.POST.get('savings')
        expenses = request.POST.get('expenses')

        # Debug prints to check if data is being captured
        print(f'User: {user}, Name: {name}, Surname: {surname}, DOB: {dob}, Mobile: {mobile}, Fixed Income: {fixed_income}, Variable Income: {variable_income}, Profession: {profession}, Insurance: {insurance}, Savings: {savings}, Expenses: {expenses}')
        if not all([name, surname, dob, mobile, fixed_income, variable_income, profession, insurance, savings, expenses]):
            # If any required field is missing, handle the error appropriately
            return render(request, 'details_form.html', {'error': 'All fields are required.'})

        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.name = name
        profile.surname = surname
        profile.dob = dob
        profile.mobile = mobile
        profile.fixed_income = fixed_income
        profile.variable_income = variable_income
        profile.profession = profession
        profile.insurance = insurance
        profile.savings = savings
        profile.expenses = expenses
        if 'image' in request.FILES:
            profile.image = request.FILES['image']
        profile.save()
        return render(request, 'details_form.html', {'userprofile': profile, 'message': 'profile details updated succesfully'})
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'details_form.html', {'userprofile':profile })

import os
from django.conf import settings
@login_required
def upload_profile_image(request):
    if request.method == 'POST':
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        if 'image' in request.FILES:
            # Delete the old image if it exists
            if user_profile.image:
                old_image_path = os.path.join(settings.MEDIA_ROOT, user_profile.image.path)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            
            # Save the new image
            user_profile.image = request.FILES['image']
            user_profile.save()
            
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'No image provided'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

from .models import UploadedFile
@login_required
def statement_upload(request):
    if request.method == 'POST':
        print("POST request received")  # Debug print

        # Get multiple files
        uploaded_files = request.FILES.getlist('file')

        if uploaded_files:
            user_profile = UserProfile.objects.get(user=request.user)
            for uploaded_file in uploaded_files:
                # Save each uploaded file
                new_file = UploadedFile(user_profile=user_profile, file=uploaded_file)
                new_file.save()
                print(f"File uploaded successfully: {uploaded_file.name}")  # Debug print

            return JsonResponse({'success': True})
        else:
            print("No files uploaded")  # Debug print
            return JsonResponse({'success': False, 'error': 'No files uploaded'})

    return render(request, 'statement_upload.html')

# views.py
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from myapp.models import UploadedFile, UserProfile
import csv
import os
import logging
from collections import defaultdict

# Set up logging
logger = logging.getLogger(__name__)

@login_required
def csv_data(request):
    # Get the current user's profile
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    # Try to get the associated UploadedFile(s)
    try:
        uploaded_files = UploadedFile.objects.filter(user_profile=user_profile)
        
        if not uploaded_files.exists():
            return JsonResponse({'error': 'No CSV files associated with your profile. Please upload one to get analytics.'}, status=404)
        
        data = []
        available_years = set()
        
        for uploaded_file in uploaded_files:
            csv_file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.file.name)
            
            # Check if file exists
            if not os.path.exists(csv_file_path):
                logger.error(f"File not found: {csv_file_path}")
                continue
            
            try:
                with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        data.append(row)
                        # Extract the year from the date
                        year = row['date'].split('-')[0]
                        available_years.add(year)
            except Exception as e:
                logger.error(f"Error reading file {csv_file_path}: {e}")
                continue
        
        return JsonResponse({'data': data, 'years': sorted(list(available_years))})
    
    except Exception as e:
        logger.error(f"Error processing CSV data: {e}")
        return JsonResponse({'error': 'An error occurred while processing your CSV files. Please try again later.'}, status=500)

@login_required
def all_expenses(request):
    return render(request, 'all_expenses.html')

@login_required
def expenses_summary(request):
    return render(request, 'expenses_summary.html')

def Stock_prediction(request):
    # news data
    googlenews = GoogleNews(lang='en', period='12h', encode='utf-8')
    googlenews.get_news('National Stock Exchange')
    news = googlenews.result(sort=True)
    news_first = news[:8]
    news_length = []
    for i in range(1, len(news)//8):
        news_length.append(news[i*8:(i*8)+8])

    # chart data
    companies = Companies.objects.all()
    # Define the symbol for NIFTY index
    symbol = '^NSEI'  # '^NSEI' is the symbol for NIFTY 50 index on Yahoo Finance

    # Define the date range
    end_date = date.today()
    start_date = end_date - timedelta(days=30)

# Fetch historical data for NIFTY index
    data = yf.download(symbol, start=start_date, end=end_date)
    labels = data._data.axes[1].tolist()

    context = {
        'companies': companies,
        'labels': labels,
        'data': data['Close'].tolist(),
        'news': news,
        'news_length': news_length,
    }

    
    

    if request.POST.get('option'):

        pk = request.POST['option']
        company = Companies.get_company_by_id(pk)

        obj = RunModel(company)

        company_symbol = company.symbol  # Replace with company.symbol if company is an object

# Define the date range
        end_date = date.today()
        start_date = end_date - timedelta(days=30)

# Fetch historical data for the company's stock
        current_data = yf.download(company_symbol, start=start_date, end=end_date)

        current_labels = current_data._data.axes[1].tolist()
        nan_ = [float('nan') for i in range(len(current_labels)-1)]
        nan_.append(current_data['Close'].tolist()[-1])

        nextDays = obj.getNext30Days()

        if current_data['Close'].tolist()[-1] > nextDays[-1]:
            color = True
        else:
            color = False

        context['nextDays'] = nextDays
        context['nextDays_data'] = nan_ + nextDays
        context['nextDays_labels'] = current_labels + list(range(1, 21))
        context['selectedOption'] = company.name
        context['current_data'] = current_data['Close'].tolist()
        context['current_labels'] = current_labels
        context['color'] = color

    return render(request, 'Stock_prediction.html', context=context)

def logout_view(request):
    logout(request)
    return redirect('dashboard_before_login')