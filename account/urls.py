from django.urls import path, include
from . import views
from .views import (
    AccountAPI,
    AccountDetailAPI,
    AccountList,
    AccountCreateView,
    AccountEditView,
    AccountLoginView
)

urlpatterns = [
    # API
    path('api', AccountAPI.as_view()),
    path('api/<int:pk>', AccountDetailAPI.as_view()),
    # LOGIN
    path('login', AccountLoginView.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),
    # ACCOUNT
    path('password', views.change_password, name='account-password'),
    path('info', views.view_account_info, name='account-info'),    
    # WEB
    path('', AccountList.as_view(), name='accounts'),
    path('add', AccountCreateView.as_view(), name='account-add'),
    path('edit/<int:pk>', AccountEditView.as_view(), name='account-edit')
]
