from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

class Role(models.Model):

      '''
      The Role entries are managed by the system,
      automatically created via a Django data migration.
      '''
      CUSTOMER = 1
      SMALL_TRADER = 2
      WHOLESALER = 3
      MANUFACTURER = 4
      ADMIN = 5
      ROLE_CHOICES = (
          (CUSTOMER, 'customer'),
          (SMALL_TRADER, 'small_trader'),
          (WHOLESALER, 'wholesaler'),
          (MANUFACTURER, 'manufacturer'),
          (ADMIN, 'admin'),
      )

      id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

      def __str__(self):
          return self.get_id_display()

class User(AbstractUser):
        username = models.CharField(max_length=100)
        roles = models.ManyToManyField(Role)
        email = models.EmailField(max_length=60, unique=True)
        name = models.CharField(max_length=100)
        joining_date = models.DateField(default=datetime.date.today)

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = ['username','roles','name',]

        def __str__(self):              # __unicode__ on Python 2
            return self.email
