from django.db import models
from django.contrib.auth.models import User
from Discounts.models import Discount
from Products.models import Product

# Create your models here.
class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    discount_id = models.ForeignKey(Discount, on_delete=models.DO_NOTHING)
    order_total = models.FloatField()
    transaction_id = models.CharField(max_length=255)
    order_date = models.DateTimeField(auto_now_add=True)
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING, default=None)