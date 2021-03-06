# Generated by Django 2.1.4 on 2019-01-23 15:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('component', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('meal_type', models.CharField(choices=[('SOUP', 'SOUP'), ('PIZZA', 'PIZZA'), ('FISH', 'FISH'), ('BURGER', 'BURGER'), ('OTHER', 'OTHER')], max_length=8)),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('description', models.ImageField(blank=True, null=True, upload_to='')),
                ('components', models.ManyToManyField(to='component.Component')),
            ],
        ),
    ]
