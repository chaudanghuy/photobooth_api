from django.db import models
from device.models import Device
from cloudinary.models import CloudinaryField

# Create your models here.
class Frame(models.Model):     
     title = models.TextField()
     device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
     photo = models.URLField(max_length=500, blank=True, null=True)     
     photo_hover = models.URLField(max_length=500, blank=True, null=True)
     position = models.TextField(default='center')
     price = models.DecimalField(max_digits=10, decimal_places=0)
     created_at = models.DateTimeField(auto_now_add=True)
     deleted_at = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return f"Frame for {self.device.name}"          
     
class CloudPhoto(models.Model):
     image = CloudinaryField('image')          