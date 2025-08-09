from django.urls import path, include
from . import views
from .views import (
    RevenueView,
    RevenueEditView
)

urlpatterns = [
    # API
    path('api/payment', views.record_payment, name='record-payment'),
    path('api/daily-revenue', views.get_daily_revenue, name='daily-revenue'),
    path('api/range-revenue', views.get_range_revenue, name='range-revenue'),
    path('api/monthly-revenue', views.get_monthly_revenue, name='monthly-revenue'),
    path('api/device-revenue', views.get_device_revenue, name='device-revenue'),
    # WEB
    path('', RevenueView.as_view(), name='revenues'),
    path('edit/<int:pk>', RevenueEditView.as_view(), name='revenue-edit')          
]