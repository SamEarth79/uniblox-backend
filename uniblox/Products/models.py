from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_price = models.FloatField()
    product_description = models.TextField()
    stock = models.IntegerField()
    product_image = models.CharField(max_length=255)    # Usually images are stored in S3 and their urls are stored in database (NoSQL preferrably)