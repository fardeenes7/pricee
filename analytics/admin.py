from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(ProductView)
admin.site.register(CategoryView)
admin.site.register(LinkClick)
