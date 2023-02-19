from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'account_type', 'is_superuser', 'is_staff', 'is_active', 'date_joined']
    fieldsets = (
        (None, {'fields': ('email', 'username','password', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
        ('Personal', {'fields': ('bio', 'account_type')}),
    )
    search_fields = ['email', 'username', 'first_name', 'last_name']
    list_filter = ['account_type', 'is_superuser', 'is_staff', 'is_active']
    ordering = ['email']
    

admin.site.register(User, CustomUserAdmin)