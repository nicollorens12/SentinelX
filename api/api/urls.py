from django.urls import path
from .views import get_history, get_history_details, saveTo_history, process_traffic,register_token, test_notification

urlpatterns = [
    path('get_history/', get_history, name='get_history'),
    path('get_history_details/', get_history_details, name='get_history_details'),
    path('saveTo_history/', saveTo_history, name='saveTo_history'),
    path('process_traffic/', process_traffic, name='process_traffic'),
    path('register-token/', register_token, name='register_token'),
    path('test-notification/', test_notification, name='test_notification'),
]
