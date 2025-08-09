from django.db import models
from device.models import Device
from cloudinary.models import CloudinaryField

# Create your models here.
class Frame(models.Model):     
     title = models.TextField()
     device_id = models.ForeignKey(Device, on_delete=models.CASCADE)
     photo = models.ImageField(upload_to='frames')     
     photo_hover = models.ImageField(upload_to='frames', default='frames/default.png')
     position = models.TextField(default='center')
     price = models.DecimalField(max_digits=10, decimal_places=0)
     created_at = models.DateTimeField(auto_now_add=True)
     deleted_at = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return f"Frame for {self.device.name}"          
     
class CloudPhoto(models.Model):
     image = CloudinaryField('image')          