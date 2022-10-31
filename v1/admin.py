from django.contrib import admin

from .models import Product, Feature, Startech, Ryans, Techland, SubCategory, Category

from .tasks import refresh_records
# Register your models here.



class ProductAdmin(admin.ModelAdmin):
    #list_display = ['title', 'status']
    list_display = ['name', 'sub_category','brand', 'model', 'best_price', 'startech', 'ryans', 'techland']
    #ordering = ['title']
    #change_list_template = 'product_change_list.html'
    actions = [refresh_records]


class TechlandAdmin(admin.ModelAdmin):
    list_display = ['link', 'price', 'regular_price', 'status', 'last_updated']
    ordering = ['last_updated']

class StartechAdmin(admin.ModelAdmin):
    list_display = ['link', 'price', 'regular_price', 'status', 'last_updated']
    ordering = ['last_updated']

class RyansAdmin(admin.ModelAdmin):
    list_display = ['link', 'price', 'regular_price', 'status', 'last_updated']
    ordering = ['last_updated']
    

admin.site.register(Product, ProductAdmin)

admin.site.register(Feature)
admin.site.register(Startech, StartechAdmin)
admin.site.register(Ryans, RyansAdmin)
admin.site.register(Techland, TechlandAdmin)
admin.site.register(SubCategory)
admin.site.register(Category)




admin.site.site_header = "Pricee Admin"
admin.site.site_title = "Pricee Admin Portal"
admin.site.index_title = "Admin Area"