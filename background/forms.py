from django import forms
from .models import Background

class BackgroundForm(forms.ModelForm):
    class Meta:
        model = Background
        fields = ['title', 'photo', 'photo_hover', 'photo_vn', 'photo_vn_hover', 'photo_kr', 'photo_kr_hover', 'position']