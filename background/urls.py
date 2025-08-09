from django.urls import path, include
from .views import (
  BackgroundAPI,
  BackgroundDetailAPI,
  BackgroundList
)

urlpatterns = [
  # API
  path('api', BackgroundAPI.as_view()),
  path('api/<int:pk>', BackgroundDetailAPI.as_view()),
  # WEB
  path('', BackgroundList.as_view(), name='backgrounds')
]
