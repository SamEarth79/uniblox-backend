from django.db import models
from django.contrib.auth.models import User
from Products.models import Product

# Create your models here.
class Cart(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)