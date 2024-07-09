from django.urls import path
from .views import login_view, signup_view, google_sign_in, home_view, logout_view, password_reset_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('google-sign-in/', google_sign_in, name='google_sign_in'),
    path('home/', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
    path('password-reset/', password_reset_view, name='password_reset'),
]
