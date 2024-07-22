from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.dashboard_before_login, name='dashboard_before_login'),
    path('csv-data/', views.csv_data, name='csv_data'),
    path('expenses-summary/', views.expenses_summary, name='expenses_summary'),
    path('all-expenses/', views.all_expenses, name='all_expenses'),
    path('upload-profile-image/', views.upload_profile_image, name='upload_profile_image'),
    path('statement_upload/', views.statement_upload, name='statement_upload'),
    path('details_form/', views.form_page, name='details_form'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('google-sign-in/', views.google_sign_in, name='google_sign_in'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('Stock_prediction/',views.Stock_prediction,name='Stock_prediction'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
