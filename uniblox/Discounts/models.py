from django.db import models

# Create your models here.
class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    discount_code = models.CharField(max_length=100)
    discount_amount = models.FloatField()