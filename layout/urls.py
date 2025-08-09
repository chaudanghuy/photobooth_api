from django.urls import path, include
from .views import (
      LayoutAPI,
      LayoutDetailAPI,
      LayoutByBackgroundAPI,
      LayoutGroupByBackgroundAPI,
      LayoutList,
      LayoutCreateView,
      LayoutEditView,
      LayoutDeleteView
  )

urlpatterns = [
      # API
      path('api', LayoutAPI.as_view()),
      path('api/<int:pk>', LayoutDetailAPI.as_view()),
      path('api/by-background/<str:background>/frame/<str:frame>', LayoutByBackgroundAPI.as_view(), name='layouts-by-background'),
      path('api/group-by-background/<int:id>/frame/<int:frame>', LayoutGroupByBackgroundAPI.as_view(), name='layouts-group-by-background'),

      # WEB
      path('', LayoutList.as_view(), name='layouts'),
      path('create', LayoutCreateView.as_view(), name='layouts-add'),
      path('edit/<int:pk>', LayoutEditView.as_view(), name='layouts-edit'),
      path('delete/<int:pk>', LayoutDeleteView.as_view(), name='layouts-delete'),
]
