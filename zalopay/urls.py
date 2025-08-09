from django.urls import path, include
from .views import (
    ZaloPayAPI,
    ZaloPayUpdateAPI,
    ZaloPayWebhookAPI,    
)


urlpatterns = [
    path('api', ZaloPayAPI.as_view()),
    path('api/update/<str:order_code>', ZaloPayUpdateAPI.as_view()),
    path('api/webhook', ZaloPayWebhookAPI.as_view()),
]
