from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from model_utils import Choices
from rest_framework.fields import ChoiceField

class Product(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_id = models.AutoField(primary_key=True)
    product_name = models.TextField(max_length=20)
    product_description = models.TextField(max_length=200)
    product_price = models.FloatField()
    product_quantity = models.IntegerField()

class Order(models.Model):
    STATUS = Choices(
        ('cart', 'cart'),
        ('delivered', 'delivered'),
        ('cancelled', 'cancelled'),)

    def delivery_time():
        return timezone.now() + timezone.timedelta(days=7)

    order = models.AutoField(primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #Customer, Trader
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_quantity = models.IntegerField()
    order_date = models.DateField(default=datetime.now())
    expected_delivery_date = models.DateTimeField(default=delivery_time)
    order_status = models.CharField(max_length=9, choices=STATUS)

    REQUIRED_FIELDS = ['product','order_status','owner']
