from django.http import HttpResponse
from django.contrib import admin
from datetime import datetime
from celery import task, shared_task
from .scripts.startech import load_from_startech, get_product_data as get_startech_product_data
from .scripts.techland import load_from_techland, get_product_data as get_techland_product_data
from .scripts.ryans import load_from_ryans, get_product_data as get_ryans_product_data
from .scripts.new import load_from_techland, get_product_data as get_new_product_data
from .models import Category, SubCategory, Link, Product

def cleancategories():
    category = Category.objects.all()
    categories = {}
    for cat in category:
        categories[cat] = []
        subcategory = SubCategory.objects.filter(category=cat)
        for subcat in subcategory:
            categories[cat].append(subcat)
    others = Category.objects.get_or_create(name="Others")[0]
    for cat in categories:
        catname = cat.name.strip().lower()
        subcategories = categories[cat]
        if len(categories[cat]) == 0:
            try:
                cat.delete()
            except:
                pass
        elif len(categories[cat]) == 1 or catname=="city it mega fair" or catname=="idb pc offer" or len(catname)>=20:
            subcategory = categories[cat][0]
            subcategory.category = others
            subcategory.save()
            try:
                cat.delete()
            except:
                pass
        elif catname!='accessories' and (catname.__contains__("accessories") or catname.__contains__("accessory") or catname.__contains__("cable") or catname.__contains__("adapter") or catname.__contains__("type-c") or catname.__contains__("usb") or catname.__contains__("pen") or catname.__contains__("gadget") or catname.__contains__("bag") or catname.__contains__("backpack") ):
            for subcategory in subcategories:
                subcategory.category = Category.objects.get_or_create(name="Accessories")[0]
                subcategory.save()
            try:
                cat.delete()
            except:
                pass
        elif catname!='home appliance' and (catname.__contains__("home") or catname.__contains__("tv") or catname.__contains__("home appliances") or ((not catname.__contains__("accessor")) and catname.__contains__("ac"))):
            for subcategory in subcategories:
                subcategory.category = Category.objects.get_or_create(name="Home Appliance")[0]
                subcategory.save()
            try:
                cat.delete()
            except:
                pass
        elif catname!='networking' and (catname.__contains__("network") or catname.__contains__("switch") or catname.__contains__("router") or catname.__contains__("modem") or catname.__contains__("server")):
            for subcategory in subcategories:
                subcategory.category = Category.objects.get_or_create(name="Networking")[0]
                subcategory.save()
            try:
                cat.delete()
            except:
                pass
        elif catname!='office items' and (catname.__contains__("office")):
            for subcategory in subcategories:
                subcategory.category = Category.objects.get_or_create(name="Office Items")[0]
                subcategory.save()
            try:
                cat.delete()
            except:
                pass
        elif catname!='gaming zone' and (catname.__contains__("gaming") or catname.__contains__("game")):
            for subcategory in subcategories:
                subcategory.category = Category.objects.get_or_create(name="Gaming Zone")[0]
                subcategory.save()
            try:
                cat.delete()
            except:
                pass
        elif catname!='laptop & tablet' and (catname.__contains__("laptop") or catname.__contains__("tablet")):
            for subcategory in subcategories:
                subcategory.category = Category.objects.get_or_create(name="Laptop & Tablet")[0]
                subcategory.save()
            try:
                cat.delete()
            except:
                pass
        elif catname!='monitor' and (catname.__contains__("monitor")):
            c = Category.objects.get_or_create(name="Monitor")[0]
            for subcategory in subcategories:
                subcategory.category = c
                subcategory.save()
            try:
                cat.delete()
            except:
                pass
        elif catname!='camera' and (catname.__contains__("camera")):
            c = Category.objects.get_or_create(name="Camera")[0]
            for subcategory in subcategories:
                subcategory.category = c
                subcategory.save()
            try:
                cat.delete()
            except:
                pass
        
        elif catname!='printer' and (catname.__contains__("printer")):
            c = Category.objects.get_or_create(name="Printer")[0]
            for subcategory in subcategories:
                subcategory.category = c
                subcategory.save()
            try:
                cat.delete()
            except:
                pass
        elif catname!='software' and (catname.__contains__("software") or catname.__contains__("graphics editing") or catname.__contains__("engineering design") ):
            c = Category.objects.get_or_create(name="Software")[0]
            for subcategory in subcategories:
                if catname.__contains__("graphics editing") or catname.__contains__("engineering design"):
                    subcategory.name = catname.capitalize()
                subcategory.category = c
                subcategory.save()
            try:
                cat.delete()
            except:
                pass
        elif catname!='desktop' and (catname.__contains__("desktop") or catname.__contains__("component") or catname.__contains__("computer") or catname.__contains__("pc") or catname.__contains__("cpu") or catname.__contains__("motherboard") or catname.__contains__("ram") or catname.__contains__("memory") or catname.__contains__("hdd") or catname.__contains__("ssd") or catname.__contains__("hard disk") or catname.__contains__("solid state drive") or catname.__contains__("power supply") or catname.__contains__("gpu") or catname.__contains__("graphics card") or catname.__contains__("case") or catname.__contains__("cabinet")):
            c = Category.objects.get_or_create(name="Desktop")[0]
            for subcategory in subcategories:
                subcategory.category = c
                subcategory.name = catname.capitalize()
                subcategory.save()
            try:
                cat.delete()
            except:
                pass
    

    
    subcategories = SubCategory.objects.all()
    for subcategory in subcategories:
        try:
            subname = subcategory.name.lower()
            if SubCategory.objects.filter(name=subcategory.name).count()>1:
                ss = SubCategory.objects.filter(name=subcategory.name)
                for s in ss:
                    if s!=subcategory:
                        pr = Product.objects.filter(sub_category=s)
                        for p in pr:
                            p.sub_category = subcategory
                            p.save()
                        s.delete()
            elif subname.__contains__("keyboard") or subname.__contains__("mouse") or subname.__contains__("headphone") or subname.__contains__("speaker") or subname.__contains__("usb") or subname.__contains__("adapter") or subname.__contains__("cable") or subname.__contains__("charger") or subname.__contains__("power bank") or subname.__contains__("bluetooth") or subname.__contains__("neckband") or subname.__contains__("tws") or subname.__contains__("hub") or subname.__contains__("dock") or subname.__contains__("converter") or subname.__contains__("dock"):
                subcategory.category = Category.objects.get_or_create(name="Accessories")[0]
                subcategory.save()
            elif subname.__contains__("monitor") or subname.__contains__("tv") or subname=="ac" or subname.__contains__("refrigerator") or subname.__contains__("washing machine") or subname.__contains__("air conditioner") or subname.__contains__("home theater") or subname.__contains__("home appliance") or subname.__contains__("home appliances"):
                subcategory.category = Category.objects.get_or_create(name="Home Appliances")[0]
                subcategory.save()
            elif subname.__contains__("cctv") or subname.__contains__("cc camera") or subname.__contains__("security camera") or subname.__contains__("security system") or subname.__contains__("security") or subname.__contains__("surveillance") or subname.__contains__("surveillance camera") or subname.__contains__("surveillance system") or subname.__contains__("dvr") or subname.__contains__("nvr") or subname.__contains__("ip camera"):
                subcategory.category = Category.objects.get_or_create(name="Security")[0]
                subcategory.save()
            elif subname.__contains__("camera") or subname.__contains__("dslr") or subname.__contains__("lens") or subname.__contains__("tripod") or subname.__contains__("action camera") or subname.__contains__("camera accessories") or subname.__contains__("gimbal")  or subname.__contains__("cam"):
                subcategory.category = Category.objects.get_or_create(name="Camera")[0]
                subcategory.save()
            elif subname.__contains__("hard disk") or subname.__contains__("harddisk") or subname.__contains__("hdd") or subname.__contains__("ssd") or subname.__contains__("solid state drive") or subname.__contains__("memory card") or subname.__contains__("sdcard") or subname.__contains__("sd card") or subname.__contains__("storage") or subname.__contains__("pendrive") or subname.__contains__("usb") or subname.__contains__("flash drive") or subname.__contains__("pen drive"):
                subcategory.category = Category.objects.get_or_create(name="Storage")[0]
                subcategory.save()
            elif subname.__contains__("laptop") or subname.__contains__("tablet") or subname.__contains__("notebook") or subname.__contains__("ultrabook") or subname.__contains__("netbook") or subname.__contains__("laptop accessories"):
                subcategory.category = Category.objects.get_or_create(name="Laptop & Tablet")[0]
                subcategory.save()
            elif subname.__contains__("printer") or subname.__contains__("scanner") or subname.__contains__("ink") or subname.__contains__("toner") or subname.__contains__("printer accessories"):
                subcategory.category = Category.objects.get_or_create(name="Printer")[0]
                subcategory.save()
            elif subname.__contains__("desktop") or subname.__contains__("component") or subname.__contains__("computer") or subname.__contains__("pc") or subname.__contains__("cpu") or subname.__contains__("motherboard") or subname.__contains__("ram") or subname.__contains__("memory") or subname.__contains__("power supply") or subname.__contains__("gpu") or subname.__contains__("graphics card") or subname.__contains__("case") or subname.__contains__("cabinet") or subname.__contains__("thermal paste") or subname.__contains__("fan") :
                subcategory.category = Category.objects.get_or_create(name="Desktop")[0]
                subcategory.save()
            elif subname.__contains__("software") or subname.__contains__("graphics editing") or subname.__contains__("engineering design"):
                subcategory.category = Category.objects.get_or_create(name="Software")[0]
                subcategory.save()
        except:
            continue    

    

    subcategories = SubCategory.objects.filter(products=None)
    for subcategory in subcategories:
        if not Product.objects.filter(sub_category=subcategory).exists():
            subcategory.delete()

    for cat in category:
        if not SubCategory.objects.filter(category=cat).exists():
            try:
                cat.delete()
            except:
                pass
        
    print("Done cleaning categories")
    return HttpResponse("Done")


# @shared_task
def refreshAllRecords():
    print("Refreshing all records")
    loadAll()
    return HttpResponse("Done")



def loadAll():
    start = datetime.now()
    load_from_techland()
    # load_from_startech()
    #load_from_ryans()
    cleancategories()
    end = datetime.now()
    time_taken = (end - start).total_seconds()
    hour = int(time_taken//3600)
    minute = int(time_taken//60) - (hour*60)
    second = int(time_taken%3600 - (minute*60))
    report = f"Total time taken: {hour} hours {minute} minutes {second} seconds"
    print("\033[1m\033[96m####################################################################")
    print("\033[1m\033[96m#####                                                          #####")
    print("\033[1m\033[96m#####      " + report + "     #####")
    print("\033[1m\033[96m#####                                                          #####")
    print("\033[1m\033[96m####################################################################")
    

def adminActionRefreshAll(request):
    refreshAllRecords.delay()
    return HttpResponse("Refreshing")


@admin.action(description='Refresh selected products')
def refresh_records(modeladmin, request, queryset):
    for query in queryset:
        links = Link.objects.filter(product=query)
        for link in links:
            if link.href.__contains__("techlandbd"):
                get_techland_product_data(link.href)
            elif link.href.__contains__("startech.com.bd"):
                get_startech_product_data(link.href)
            elif link.href.__contains__("ryanscomputers.com"):
                get_ryans_product_data(link.href)
        cleancategories()


@admin.action(description='Clean categories')
def clean_categories(modeladmin, request, queryset):
    cleancategories()




#celery -A pricee worker -l info