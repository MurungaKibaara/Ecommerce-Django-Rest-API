# Generated by Django 3.0.3 on 2020-03-01 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_product_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]