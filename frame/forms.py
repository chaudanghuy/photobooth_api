from django import forms
from .models import Frame, CloudPhoto
from cloudinary.forms import CloudinaryFileField

class FrameForm(forms.ModelForm):
    class Meta:
        model = Frame
        fields = ['device_id', 'title', 'photo', 'photo_hover', 'position', 'price']
        
class PhotoForm(forms.ModelForm):
    model = CloudPhoto
    fields = '__all__'
    
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['image'].options={
           'tags': 'new_image',
           'format': 'png'
    }
