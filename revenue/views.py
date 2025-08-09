import requests, json
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from .models import Order, Transaction
from device.models import Device
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here. 

@csrf_exempt
def record_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body);
        device_id = data.get('device_id')
        amount = data.get('amount')
        try:
            order = Order.objects.get(device_id=device_id, status='pending')
            transaction = Transaction(order_id=order, amount=amount, transaction_status='success')
            transaction.save()
            order.status = 'paid'
            order.save()
            return JsonResponse({'message': 'Payment recorded successfully'}, status=status.HTTP_201_CREATED)
        except Order.DoesNotExist:
            return JsonResponse({'message': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    return JsonResponse({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        
def get_daily_revenue(request):
    if request.method == 'GET':
        transactions = Transaction.objects.filter(status='paid')
        daily_revenue = {}
        for transaction in transactions:
            date = transaction.created_at.date()
            if date in daily_revenue:
                daily_revenue[date] += transaction.total_price
            else:
                daily_revenue[date] = transaction.total_price
        return JsonResponse(daily_revenue, status=status.HTTP_200_OK)
    return JsonResponse({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

def get_range_revenue(request):
    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        transactions = Transaction.objects.filter(status='paid', created_at__range=[start_date, end_date])
        range_revenue = 0
        for transaction in transactions:
            range_revenue += transaction.total_price
        return JsonResponse({'revenue': range_revenue}, status=status.HTTP_200_OK)
    return JsonResponse({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

def get_monthly_revenue(request):
    if request.method == 'GET':
        transactions = Transaction.objects.filter(status='paid')
        monthly_revenue = {}
        for transaction in transactions:
            month = transaction.created_at.strftime('%B')
            if month in monthly_revenue:
                monthly_revenue[month] += transaction.total_price
            else:
                monthly_revenue[month] = transaction.total_price
        return JsonResponse(monthly_revenue, status=status.HTTP_200_OK)
    return JsonResponse({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

def get_device_revenue(request):
    if request.method == 'GET':
        device_id = request.GET.get('device_id')
        transactions = Transaction.objects.filter(status='paid', device_id=device_id)
        device_revenue = 0
        for transaction in transactions:
            device_revenue += transaction.total_price
        return JsonResponse({'revenue': device_revenue}, status=status.HTTP_200_OK)
    return JsonResponse({'message': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

class RevenueView(LoginRequiredMixin, View):
    def get(self, request):
        device_id = request.GET.get('device_id')
        if device_id:
            revenues = Transaction.objects.filter(device_id=device_id, status='paid')
        else:
            revenues = Transaction.objects.all()
        devices = Device.objects.all()
        return render(request, 'revenues/list.html', {'revenues': revenues, 'devices': devices})

class RevenueEditView(LoginRequiredMixin, View):
    def get(self, request):
        # revenue = requests.get(f'http://localhost:8000/revenues/{request.GET.get("id")}')
        # get first transaction
        revenue = Transaction.objects.first()
        return render(request, 'revenues/edit.html', {'revenue': revenue})        