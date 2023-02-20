from django.contrib import admin
from .views import *
# Register your models here.

class BannerAdAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'body')
    prepopulated_fields = {'slug': ('title',)}
    

admin.site.register(BannerAd, BannerAdAdmin)