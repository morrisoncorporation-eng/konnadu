# Generated by Django 3.2.7 on 2021-12-14 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_cart_shipping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='currency',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
