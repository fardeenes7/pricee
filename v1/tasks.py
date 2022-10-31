from http.client import HTTPResponse
from django.contrib import admin
from datetime import datetime
from celery import task, shared_task
from .loadFromStartech import load_from_startech, get_product_data as get_startech_product_data
from .loadFromTechland import load_from_techland, get_product_data as get_techland_product_data
from .loadFromRyans import load_from_ryans, get_product_data as get_ryans_product_data

@shared_task
def refreshAllRecords():
    return loadAll()


def loadAll():
    start = datetime.now()
    load_from_techland()
    load_from_startech()
    load_from_ryans()
    end = datetime.now()
    print("Time taken to load all records: ", end - start)

def adminActionRefreshAll(request):
    refreshAllRecords.delay()
    return HTTPResponse("Refreshing")



@admin.action(description='Refresh selected products')
def refresh_records(modeladmin, request, queryset):
    for query in queryset:
        get_startech_product_data(query.startech.link)
        get_techland_product_data(query.techland.link)
        get_ryans_product_data(query.ryans.link)

#celery -A pricee worker -l info