# Generated by Django 2.1.3 on 2018-12-11 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('amount', models.SmallIntegerField()),
                ('price_per_dish', models.SmallIntegerField()),
                ('component_type', models.CharField(choices=[('MEAT', 'MEAT'), ('CHEESE', 'CHEESE'), ('VEGETABLE', 'VEGETABLE'), ('FRUIT', 'FRUIT'), ('OTHER', 'OTHER')], max_length=10)),
            ],
        ),
    ]
