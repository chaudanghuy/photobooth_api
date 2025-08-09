from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'method', 'name', 'code', 
            'appID', 'key1', 'key2', 
            'endpoint_sandbox', 'endpoint_prod', 'token',
            'username', 'password',
            'is_active'
        ]