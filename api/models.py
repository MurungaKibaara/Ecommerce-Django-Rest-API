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
        ('confirmed', 'confirmed'),
        ('to_deliver', 'to_deliver'),
        ('delivered', 'delivered'),
        ('cancelled', 'cancelled'),)

    order = models.AutoField(primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_quantity = models.IntegerField()
    order_date = models.DateTimeField(default=timezone.now)
    order_status = models.CharField(max_length=10, choices=STATUS)

    REQUIRED_FIELDS = ['product_id','order_status','owner']

class Sale(models.Model):

    def order_delivery_date():
        return timezone.now() + timezone.timedelta(days=7)

    SALE_STATUS = Choices(
        ('confirmed', 'confirmed'),
        ('to_deliver', 'to_deliver'),
        ('delivered', 'delivered'),
        ('cancelled', 'cancelled'),)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    delivery_id =  models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    confirm_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField(default=order_delivery_date)
    reference = models.CharField(max_length=20, unique=True)
    order_status = models.CharField(max_length=10, choices=SALE_STATUS)

    REQUIRED_FIELDS = ['order_id','owner','order_status']
