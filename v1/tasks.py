from http.client import HTTPResponse
from django.contrib import admin
from datetime import datetime
from celery import task, shared_task
from .loadFromStartech import load_from_startech, get_product_data as get_startech_product_data
from .loadFromTechland import load_from_techland, get_product_data as get_techland_product_data
from .loadFromRyans import load_from_ryans, get_product_data as get_ryans_product_data
from .models import Category, SubCategory

def cleancategories():
    category = Category.objects.all()
    categories = {}
    for cat in category:
        categories[cat.name] = []
        subcategory = SubCategory.objects.filter(category=cat)
        for subcat in subcategory:
            categories[cat.name].append(subcat.name)
    other = Category.objects.get(name="Other") if Category.objects.filter(name="Other").exists() else Category.objects.create(name="Other")
    #other = Category.objects.filter(name="Other")
    for cat in categories:
        if len(categories[cat]) == 0:
            category = Category.objects.filter(name=cat)
            print("***Deleting category: ", cat, " ***")
            category.delete()
        elif len(categories[cat]) == 1:
            category = Category.objects.filter(name=cat)
            subcategory = SubCategory.objects.get(category=category[0])
            subcategory.category = other
            subcategory.save()
            category.delete()
    return HTTPResponse("Done")



@shared_task
def refreshAllRecords():
    return loadAll()


def loadAll():
    start = datetime.now()
    load_from_techland()
    load_from_startech()
    load_from_ryans()
    cleancategories()
    end = datetime.now()
    print("Time taken to load all records: ", end - start)

def adminActionRefreshAll(request):
    refreshAllRecords.delay()
    return HTTPResponse("Refreshing")







@admin.action(description='Refresh selected products')
def refresh_records(modeladmin, request, queryset):
    for query in queryset:
        get_startech_product_data(query.startech.link) if query.startech else None
        get_techland_product_data(query.techland.link) if query.techland else None
        get_ryans_product_data(query.ryans.link) if query.ryans else None




#celery -A pricee worker -l info