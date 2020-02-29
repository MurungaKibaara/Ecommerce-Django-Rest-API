from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.AutoField(primary_key=True)
    product_name = models.TextField(max_length=20)
    product_description = models.TextField(max_length=200)
    product_price = models.FloatField()
    product_quantity = models.IntegerField()
    slug = models.SlugField(max_length=200 , db_index = True , unique= True)

    def __str__(self):
        return self.__all__
