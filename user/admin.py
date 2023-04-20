from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'name', 'account_type', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'auth_provider']
    fieldsets = (
        (None, {'fields': ('email', 'username','password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
        ('Personal', {'fields': ('bio', 'account_type', 'profile_pic')}),
    )
    search_fields = ['email', 'username']
    list_filter = ['account_type', 'is_superuser', 'is_staff', 'is_active']
    ordering = ['email']
    

admin.site.register(User, CustomUserAdmin)