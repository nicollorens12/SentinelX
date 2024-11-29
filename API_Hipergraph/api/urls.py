from django.urls import path
from .views import get_history, get_history_details, saveTo_history

urlpatterns = [
    path('get_history/', get_history, name='get_history'),
    path('get_history_details/', get_history_details, name='get_history_details'),
    path('saveTo_history/', saveTo_history, name='saveTo_history'),
]
