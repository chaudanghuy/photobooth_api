from django.db import models

# Create your models here.
class Payment(models.Model):
    method = models.TextField()
    name = models.TextField()
    code = models.TextField(unique=True, default="zalopay")
    appID = models.TextField(default="2553")
    key1 = models.TextField(default="PcY4iZIKFCIdgZvA6ueMcMHHUbRLYjPL")
    key2 = models.TextField(default="kLtgPl8HHhfvMuDHPwKfgfsY4Ydm9eIz")
    endpoint_sandbox = models.TextField(default="https://sb-openapi.zalopay.vn/v2/create")
    endpoint_prod = models.TextField(default="https://openapi.zalopay.vn/v2/create")
    token = models.TextField(default="123")
    username = models.TextField(default="account-demo")
    password = models.TextField(default="123")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Payment Method {self.name}"