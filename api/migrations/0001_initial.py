# Generated by Django 3.0.3 on 2020-03-02 12:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order', models.AutoField(primary_key=True, serialize=False)),
                ('order_quantity', models.IntegerField()),
                ('order_date', models.DateField(default=django.utils.timezone.now)),
                ('order_status', models.CharField(choices=[('cart', 'cart'), ('confirmed', 'confirmed'), ('to_deliver', 'to_deliver'), ('delivered', 'delivered'), ('cancelled', 'cancelled')], max_length=10)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('delivery_id', models.AutoField(primary_key=True, serialize=False)),
                ('confirm_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('delivery_date', models.DateTimeField()),
                ('reference', models.CharField(max_length=20, unique=True)),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Order')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.TextField(max_length=20)),
                ('product_description', models.TextField(max_length=200)),
                ('product_price', models.FloatField()),
                ('product_quantity', models.IntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Product'),
        ),
    ]
