from django.urls import path, include
from .views import (
    StoreAPI,
    StoreDetailAPI,
    StoreListView,
    AddStoreView,
    EditStoreView
)

urlpatterns = [
    # API
    path('api', StoreAPI.as_view()),
    path('api/<int:pk>', StoreDetailAPI.as_view()),
    # Store
     path('', StoreListView.as_view(), name='stores'),
     path('add', AddStoreView.as_view(), name='stores-add'),
     path('edit/<int:pk>', EditStoreView.as_view(), name='stores-edit')     
]