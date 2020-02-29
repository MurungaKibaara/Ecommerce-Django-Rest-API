# Generated by Django 3.0.3 on 2020-02-29 20:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.TextField(max_length=20)),
                ('product_description', models.TextField(max_length=200)),
                ('product_price', models.FloatField()),
                ('product_quantity', models.IntegerField()),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
