from django.http import HttpResponse
from django.contrib import admin
from datetime import datetime
from celery import task, shared_task
from .scripts.startech import load_from_startech, get_product_data as get_startech_product_data
from .scripts.techland import load_from_techland, get_product_data as get_techland_product_data
from .scripts.ryans import load_from_ryans, get_product_data as get_ryans_product_data
from .models import Category, SubCategory

def cleancategories():
    category = Category.objects.all()
    categories = {}
    for cat in category:
        categories[cat] = []
        subcategory = SubCategory.objects.filter(category=cat)
        for subcat in subcategory:
            categories[cat].append(subcat)
    
    others = Category.objects.get_or_create(name="Others")[0]
    #other = Category.objects.filter(name="Other")
    for cat in category:
        print("Category: ", cat.name, " Subcategories: ", len(categories[cat]))
        if len(categories[cat]) == 0:
            print("***Deleting category: ", cat, " ***")
            cat.delete()
        elif cat.name=='Others' and (len(categories[cat]) == 1 or cat.name=="City IT Mega Fair" or cat.name=="IDB PC Offer"):
            subcategory = categories[cat][0]
            subcategory.category = others
            subcategory.save()
            cat.delete()
        elif cat.name.lower()!='accessories' and (cat.name.lower().__contains__("accessories") or cat.name.lower().__contains__("accessory")):
            subcategories = categories[cat]
            for subcategory in subcategories:
                subcategory.category = Category.objects.get_or_create(name="Accessories")[0]
                subcategory.save()
            cat.delete()
        elif cat.name.lower()!='gaming zone' and (cat.name.lower().__contains__("gaming")):
            subcategories = categories[cat]
            for subcategory in subcategories:
                subcategory.category = Category.objects.get_or_create(name="Gaming Zone")[0]
                subcategory.save()
            cat.delete()
        elif cat.name.lower()!='laptop & tablet' and (cat.name.lower().__contains__("laptop") or cat.name.lower().__contains__("tablet")):
            subcategories = categories[cat]
            for subcategory in subcategories:
                subcategory.category = Category.objects.get_or_create(name="Laptop & Tablet")[0]
                subcategory.save()
            cat.delete()
        elif cat.name.lower()!='monitor' and (cat.name.lower().__contains__("monitor")):
            subcategories = categories[cat]
            c = Category.objects.get_or_create(name="Monitor")[0]
            for subcategory in subcategories:
                subcategory.category = c
                subcategory.save()
            cat.delete()
        elif cat.name.lower()!='software' and (cat.name.lower().__contains__("printer")):
            subcategories = categories[cat]
            c = Category.objects.get_or_create(name="Printer")[0]
            for subcategory in subcategories:
                subcategory.category = c
                subcategory.save()
            cat.delete()
        elif cat.name.lower()!='software' and (cat.name.lower().__contains__("software")):
            subcategories = categories[cat]
            Category.objects.get_or_create(name="Software")[0]
            for subcategory in subcategories:
                subcategory.category = c
                subcategory.save()
            cat.delete()
        elif cat.name.lower()!='desktop' and (cat.name.lower().__contains__("desktop") or cat.name.lower().__contains__("component") or cat.name.lower().__contains__("computer") or cat.name.lower().__contains__("pc")):
            subcategories = categories[cat]
            c = Category.objects.get_or_create(name="Desktop")[0]
            for subcategory in subcategories:
                subcategory.category = c
                subcategory.save()
            cat.delete()
        
    print("Done cleaning categories")
    return HttpResponse("Done")



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
    time_taken = (end - start).total_seconds()
    print("\033[1m\033[96m#########################################")
    print()
    print("\033[1m\033[96mTime taken to load all records: ", int(time_taken//3600), " hours ", int(time_taken//60), " minutes ", time_taken%3600, " seconds")
    print()
    print("\033[1m\033[96m#########################################")
    

def adminActionRefreshAll(request):
    refreshAllRecords.delay()
    return HttpResponse("Refreshing")


@admin.action(description='Refresh selected products')
def refresh_records(modeladmin, request, queryset):
    for query in queryset:
        get_startech_product_data(query.startech.link) if query.startech else None
        get_techland_product_data(query.techland.link) if query.techland else None
        get_ryans_product_data(query.ryans.link) if query.ryans else None
        cleancategories()


@admin.action(description='Clean categories')
def clean_categories(modeladmin, request, queryset):
    cleancategories()




#celery -A pricee worker -l info