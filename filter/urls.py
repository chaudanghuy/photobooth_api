from django.urls import path, include
from .views import (
    FilterAPI,
    FilterDetailAPI,
    FilterList,
    FilterCreateView,
    FilterEditView,
    FilterDeleteView
)

urlpatterns = [
    # API
    path('api', FilterAPI.as_view()),
    path('api/<int:pk>', FilterDetailAPI.as_view()),
    # WEB
    path('', FilterList.as_view(), name='filters'),
    path('add', FilterCreateView.as_view(), name='filters-add'),
    path('edit/<int:pk>', FilterEditView.as_view(), name='filters-edit'),
    path('delete/<int:pk>', FilterEditView.as_view(), name='filters-delete'),
]