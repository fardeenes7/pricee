from django.contrib import admin

from .models import Product, Feature, SubCategory, Category, Link, Shop

from .tasks import refresh_records, clean_categories
# Register your models here.



class ProductAdmin(admin.ModelAdmin):
    #list_display = ['title', 'status']
    list_display = ['name', 'slug', 'sub_category','brand', 'model', 'best_price']
    #ordering = ['title']
    #change_list_template = 'product_change_list.html'
    actions = [refresh_records]


class LinkAdmin(admin.ModelAdmin):
    list_display = ['product', 'shop', 'price', 'status']
    ordering = ['product']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    ordering = ['name']
    actions = [clean_categories]


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'slug']
    ordering = ['category']
    

admin.site.register(Product, ProductAdmin)

admin.site.register(Feature)
admin.site.register(Link, LinkAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Shop)




admin.site.site_header = "Pricee Admin"
admin.site.site_title = "Pricee Admin Portal"
admin.site.index_title = "Admin Area"