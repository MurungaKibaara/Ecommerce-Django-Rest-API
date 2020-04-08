from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from model_utils import Choices
from rest_framework.fields import ChoiceField


# Product Related

class Category(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_id = models.AutoField(primary_key=True)
    product_name = models.TextField(max_length=20)
    product_description = models.TextField(max_length=200)
    product_price = models.DecimalField(max_digits=5, decimal_places=2)
    product_quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    image = models.ImageField(max_length=100, upload_to=settings.MEDIA_ROOT+'images/%Y/%m/%d/', null=True)
    # image = models.ImageField(upload_to=settings.MEDIA_ROOT, null=True, blank=True)

    def __str__(self):
        return self.product_name

# Orders - Cart
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
    order_status = models.CharField(max_length=10, choices=STATUS)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['product_id','order_status','owner']



# Order-Processing -- Sales
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
    confirm_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(default=order_delivery_date)
    reference = models.CharField(max_length=20, unique=True)
    order_status = models.CharField(max_length=10, choices=SALE_STATUS)
    updated = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['order_id','owner','order_status']
