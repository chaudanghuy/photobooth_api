from django.db import models
from background.models import Background
from frame.models import Frame

# Create your models here.
class Layout(models.Model):
    title = models.TextField()
    background = models.ForeignKey(Background, on_delete=models.CASCADE)
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE, blank=True, null=True)
    photo = models.ImageField(upload_to='layouts')
    photo_cover = models.ImageField(upload_to='layouts', default='layouts/default.png')
    photo_full = models.ImageField(upload_to='layouts', default='layouts/default.png')
    position = models.TextField(default='center')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Layout {self.title}"