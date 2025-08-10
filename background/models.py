from django.db import models
from frame.models import Frame

# Create your models here.
class Background(models.Model):
    title = models.TextField()
    photo = models.ImageField(upload_to='backgrounds')
    photo_hover = models.URLField(max_length=500, blank=True, null=True)
    photo_vn = models.URLField(max_length=500, blank=True, null=True)
    photo_vn_hover = models.URLField(max_length=500, blank=True, null=True)
    photo_kr = models.URLField(max_length=500, blank=True, null=True)
    photo_kr_hover = models.URLField(max_length=500, blank=True, null=True)
    position = models.TextField(default='center')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title