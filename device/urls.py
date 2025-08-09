from django.urls import path, include
from .views import (
     DeviceAPI,
     DeviceDetailAPI,
     DeviceList,
     DeviceCreateView,
     DeviceEditView
)

urlpatterns = [
     # API
     path('api', DeviceAPI.as_view()),
     path('api/<int:pk>', DeviceDetailAPI.as_view()),
     # WEB
     path('', DeviceList.as_view(), name='devices'),
     path('add', DeviceCreateView.as_view(), name='devices-add'),
     path('edit/<int:pk>', DeviceEditView.as_view(), name='devices-edit')          
]