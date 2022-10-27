from django.contrib import admin
from django.urls import path
from .views import refreshAllRecords, viewAllRecords
from .tasks import adminActionRefreshAll

urlpatterns = [
    path('refreshAllRecords/', refreshAllRecords, name='refreshAllRecords'),
    path('all/', viewAllRecords, name='viewAllRecords'),
]
