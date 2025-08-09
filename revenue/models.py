from django.db import models
from device.models import Device
from payment.models import Payment

# Create your models here.
class Order(models.Model):
    order_code = models.CharField(max_length=100)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
    product_price = models.FloatField()
    base_price = models.FloatField()
    tax = models.FloatField()
    total_price = models.FloatField()
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo_url_done = models.TextField(default='')

    def __str__(self):
        return f"Order #{self.order_code} with {self.total_price}"
    
class Transaction(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE)
    amount = models.FloatField()
    transaction_status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction total {self.amount} for order ${self.order_id.order_code}"
