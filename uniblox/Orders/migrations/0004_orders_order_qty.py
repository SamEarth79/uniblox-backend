# Generated by Django 4.2.17 on 2024-12-27 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0003_orders_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='order_qty',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
