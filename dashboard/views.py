from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from revenue.models import Order, Transaction
from device.models import Device
from store.models import Store
from django.shortcuts import get_object_or_404

# Create your views here.

class Dashboard(LoginRequiredMixin, View):    
    def get(self, request):
        device_id = request.GET.get('device')
        device = None
        devices = Device.objects.all()

        transactions = []
        total_amount = 0

        if device_id:
            # Show data for a specific device
            device = get_object_or_404(Device, id=device_id)
            orders = Order.objects.filter(device_id=device.id)
            transactions = (
                Transaction.objects
                .filter(order_id__device_id=device.id)
                .select_related('order_id', 'order_id__device_id', 'payment_id')
                .order_by('-id')
            )
        else:
            # Show data for all devices
            orders = Order.objects.all()
            transactions = (
                Transaction.objects
                .select_related('order_id', 'order_id__device_id', 'payment_id')
                .order_by('-id')
            )

        total_amount = sum(t.amount for t in transactions)

        return render(request, 'dashboard-stores.html', {
            'device': device,
            'device_id': device_id,
            'devices': devices,
            'total_amount': total_amount,
            'transactions': transactions,
        })                