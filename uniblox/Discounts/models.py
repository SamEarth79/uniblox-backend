from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    discount_code = models.CharField(max_length=100)
    discount_percentage = models.FloatField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)