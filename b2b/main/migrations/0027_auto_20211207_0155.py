# Generated by Django 3.2.9 on 2021-12-07 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_jumbotron'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='is_exclusive',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='store',
            name='popular',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='store',
            name='trending',
            field=models.BooleanField(default=False),
        ),
    ]
