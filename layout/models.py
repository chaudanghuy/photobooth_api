from django.db import models
from background.models import Background
from frame.models import Frame

# Create your models here.
class Layout(models.Model):
    title = models.TextField()
    background = models.ForeignKey(Background, on_delete=models.CASCADE)
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE, blank=True, null=True)
    photo = models.URLField(max_length=500, blank=True, null=True)
    photo_cover = models.URLField(max_length=500, blank=True, null=True)
    photo_full = models.URLField(max_length=500, blank=True, null=True)
    position = models.TextField(default='center')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Layout {self.title}"