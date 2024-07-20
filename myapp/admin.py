# admin.py
from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'surname', 'dob', 'mobile', 'fixed_income', 'variable_income', 'profession', 'insurance', 'savings', 'expenses', 'image')
    search_fields = ('user__username','name', 'surname', 'mobile')
    list_filter = ('dob', 'profession')

admin.site.register(UserProfile, UserProfileAdmin)
