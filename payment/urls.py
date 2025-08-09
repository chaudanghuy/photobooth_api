from django.urls import path, include
from .views import (
    PaymentAPI,
    PaymentDetailAPI,
    PaymentList,
    PaymentCreateView,
    PaymentEditView,
    PaymentDeleteView
)
from .views import start_cash_pay, stop_cash_pay, create_cash_order, webhook_cash_api, redeem_pay

urlpatterns = [
    # API
    path('api/list', PaymentAPI.as_view()),    
    path('api', PaymentAPI.as_view()),    
    path('api/<int:pk>', PaymentDetailAPI.as_view()), 

    # Cash
    path('api/cash/start', start_cash_pay, name='start_cash_pay'),
    path('api/cash/create', create_cash_order, name='stop_cash_pay'),
    path('api/cash/webhook', webhook_cash_api, name='create_cash_order'),
    path('api/cash/stop', stop_cash_pay, name='webhook_cash_api'),
    path('api/redeem', redeem_pay, name='redeem_pay'),
     
    # WEB
    path('', PaymentList.as_view(), name='payments'),
    path('add', PaymentCreateView.as_view(), name='payments-add'),
    path('edit/<int:pk>', PaymentEditView.as_view(), name='payments-edit'),
    path('delete/<int:pk>', PaymentDeleteView.as_view(), name='payments-delete'),
]