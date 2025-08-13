from django.db import models

# Create your models here.
class Sticker(models.Model):
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=100)    
    photo = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']