from django.urls import path
from .views import (
    Dashboard,
    DashboardStores
)

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('device/<int:deviceID>', DashboardStores.as_view(), name='dashboard-stores'),
]