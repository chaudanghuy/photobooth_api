from django.db import models
from django.contrib.auth.models import User
from store.models import Store

# Create your models here.
class Device(models.Model):
     name = models.CharField(max_length=100)
     code = models.TextField()
     store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
     photo_shooting_time = models.TextField()
     photo_suffer_time = models.TextField()
     photo_work_time = models.TextField()
     product_price = models.TextField()
     contact_number = models.TextField(default='88888888')     
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     status = models.CharField(max_length=100, default='Online')
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     
     def __str__(self):
          return self.name
     
     class Meta:
          ordering = ['-created_at']