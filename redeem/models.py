from django.db import models

# Create your models here.
class Redeem(models.Model):
  code = models.CharField(max_length=20)
  amount = models.DecimalField(max_digits=10, decimal_places=0)
  expired_at = models.DateTimeField()
  created_at = models.DateTimeField(auto_now_add=True)
  is_used = models.BooleanField(default=False)
  date_used = models.DateTimeField(null=True)
  is_active = models.BooleanField(default=True)