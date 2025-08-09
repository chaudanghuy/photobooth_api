from django.db import models

# Create your models here.
class Sticker(models.Model):
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=100)    
    photo = models.ImageField(upload_to='stickers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']