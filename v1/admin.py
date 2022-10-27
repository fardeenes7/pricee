from django.contrib import admin

from .models import Product, Feature, Startech, Ryans, Techland

from .tasks import refresh_records
# Register your models here.



class ProductAdmin(admin.ModelAdmin):
    #list_display = ['title', 'status']
    list_display = ['name','brand', 'model', 'best_price', 'startech', 'ryans', 'techland']
    #ordering = ['title']
    #change_list_template = 'admin/product_change_list.html'
    actions = [refresh_records]

admin.site.register(Product, ProductAdmin)

admin.site.register(Feature)
admin.site.register(Startech)



admin.site.site_header = "Pricee Admin"
admin.site.site_title = "Pricee Admin Portal"
admin.site.index_title = "Admin Area"