# admin.py
from django.contrib import admin
from .models import UserProfile, UploadedFile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'surname', 'dob', 'mobile', 'fixed_income', 'variable_income', 'profession', 'insurance', 'savings', 'expenses', 'image')
    search_fields = ('user__username','name', 'surname', 'mobile')
    list_filter = ('dob', 'profession')

admin.site.register(UserProfile, UserProfileAdmin)

class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'file', 'uploaded_at')

    def get_user(self, obj):
        return obj.user_profile.name  # Or obj.profile.user.email, etc.
    get_user.short_description = 'User'  # This sets the column header in the admin interface

admin.site.register(UploadedFile, UploadedFileAdmin)