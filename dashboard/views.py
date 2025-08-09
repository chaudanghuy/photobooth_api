from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from revenue.models import Order, Transaction
from device.models import Device
from store.models import Store

# Create your views here.

class Dashboard(LoginRequiredMixin, View):    
    def get(self, request):
        
        # List stores
        stores = Store.objects.all()
        
        # List devices by store
        devices = Device.objects.all()               
        
        return render(request, 'dashboard.html', {
            'stores': stores,
            'devices': devices,            
        })            
        

class DashboardStores(LoginRequiredMixin, View):
    def get(self, request, deviceID):
        # Get store device by store id
        device = Device.objects.get(id=deviceID)
        
        if (device):
            # Get list orders by device id
            orders = Order.objects.filter(device_id=device.id).all()
            
            # Get list transaction by order id
            transactions = Transaction.objects.filter(order_id__in=orders).order_by('-id')
            total_amount = sum(t.amount for t in transactions)
            
            return render(request, 'dashboard-stores.html', {
                'device': device,
                'total_amount': total_amount,
                'transactions': transactions
            })
        return render(request, 'dashboard-stores.html')