from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from model_utils import Choices
from rest_framework.fields import ChoiceField

class User(AbstractUser):

    ROLES = Choices(('customer', 'customer'),('trader', 'trader'),('wholesaler', 'wholesaler'),('manufacturer', 'manufacturer'),('a', 'admin'),)

    role = models.CharField(max_length=12, choices=ROLES)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=60, unique=True)
    name = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','role','name',]

    def __str__(self):
        return self.email
