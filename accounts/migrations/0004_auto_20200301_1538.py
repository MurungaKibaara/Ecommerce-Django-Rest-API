# Generated by Django 3.0.3 on 2020-03-01 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200301_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='joining_date',
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('customer', 'customer'), ('trader', 'trader'), ('wholesaler', 'wholesaler'), ('manufacturer', 'manufacturer'), ('admin', 'admin')], default='customer', max_length=12),
        ),
    ]