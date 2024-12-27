from django.db import models
from django.contrib.auth.models import User
from Discounts.models import Discount

# Create your models here.
class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    discount_id = models.ForeignKey(Discount, on_delete=models.DO_NOTHING)