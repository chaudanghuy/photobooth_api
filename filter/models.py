from django.db import models

# Create your models here.
class Filter(models.Model):
    title = models.TextField()
    photo = models.ImageField(upload_to='filters/photos/')
    color_mode = models.TextField()    
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Filter for {self.device.name}"