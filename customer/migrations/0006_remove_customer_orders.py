# Generated by Django 2.1.3 on 2018-12-12 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_auto_20181212_2236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='orders',
        ),
    ]
