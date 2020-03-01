from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Product(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_id = models.AutoField(primary_key=True)
    product_name = models.TextField(max_length=20)
    product_description = models.TextField(max_length=200)
    product_price = models.FloatField()
    product_quantity = models.IntegerField()
