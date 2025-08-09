from django import forms
from .models import Redeem

class RedeemForm(forms.ModelForm):
  class Meta:
    model = Redeem
    fields = [
      'code', 'amount', 'expired_at', 'is_active'
    ]