from django.db import models
from frame.models import Frame

# Create your models here.
class Background(models.Model):
    title = models.TextField()
    photo = models.ImageField(upload_to='backgrounds')
    photo_hover = models.ImageField(upload_to='backgrounds', default='backgrounds/default.png')
    photo_vn = models.ImageField(upload_to='backgrounds', default='backgrounds/default.png')
    photo_vn_hover = models.ImageField(upload_to='backgrounds', default='backgrounds/default.png')
    photo_kr = models.ImageField(upload_to='backgrounds', default='backgrounds/default.png')
    photo_kr_hover = models.ImageField(upload_to='backgrounds', default='backgrounds/default.png')
    position = models.TextField(default='center')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title