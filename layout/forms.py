from django import forms
from .models import Layout

class LayoutForm(forms.ModelForm):
  class Meta:
    model = Layout
    fields = ['title', 'background', 'frame', 'photo', 'photo_cover', 'photo_full', 'position']