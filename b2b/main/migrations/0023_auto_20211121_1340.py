# Generated by Django 3.2.9 on 2021-11-21 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_siteconfiguration_coin_base_api_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cancelled',
        ),
        migrations.RemoveField(
            model_name='order',
            name='fulfilled',
        ),
    ]
