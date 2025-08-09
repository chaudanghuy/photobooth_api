from django.urls import path, include
from .views import (
  RedeemView,
  RedeemCreateView,
  RedeemEditView,
  RedeemDeleteView,
  RedeemListAPI,
  RedeemCodeAPI
)

urlpatterns = [
  # API
  path('api/list', RedeemListAPI.as_view()),
  path('api/<str:code>', RedeemCodeAPI.as_view()),
  
  # WEB    
  path('', RedeemView.as_view(), name='redeems'),
  path('add', RedeemCreateView.as_view(), name='redeems-add'),
  path('edit/<int:pk>', RedeemEditView.as_view(), name='redeems-edit'),
  path('delete/<int:pk>', RedeemDeleteView.as_view(), name='redeems-delete'),
]
