from django.urls import path
from .views import get_history, get_history_details, get_history_more_datails, process_traffic

urlpatterns = [
    path('get_history/', get_history, name='get_history'),
    path('get_history_details/<str:document_id>/', get_history_details, name='get_history_details'),
    path('get_history_more_datails/<str:document_id>/', get_history_more_datails, name='get_history_more_datails'),
    path('process_traffic/', process_traffic, name='process_traffic'),
]
