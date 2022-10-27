from http.client import HTTPResponse
from django.contrib import admin
from celery import task, shared_task
from .loadFromStartech import load_from_startech, get_product_data


@shared_task
def refreshAllRecords():
    return load_from_startech()



def adminActionRefreshAll(request):
    refreshAllRecords.delay()
    return HTTPResponse("Refreshing")



@admin.action(description='Refresh selected products')
def refresh_records(modeladmin, request, queryset):
    for query in queryset:
        get_product_data(query.startech.link)
