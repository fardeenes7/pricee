from http.client import HTTPResponse
import json
from django.shortcuts import render
from . import tasks
from django.http import HttpResponse as HTTPResponse
from .models import Product
# Create your views here.


def indexView(request):
    return render(request, 'index.html')

def refreshAllRecords(request):
    print("Refreshing All Records")
    tasks.refreshAllRecords.delay()
    return HTTPResponse("Refreshing All Records")



def viewAllRecords(request):
    # return json of all Product recordss
    products = Product.objects.all()
    return HTTPResponse(products)
