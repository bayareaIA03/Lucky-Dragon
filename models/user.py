from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    user_phone_number = models.CharField(max_length=20, unique=True)
    user_street_number = models.CharField(max_length=10, null=True, blank=True)
    user_street = models.CharField(max_length=50, null=True, blank=True)
    user_apt = models.CharField(max_length=10, null=True, blank=True)
    user_city = models.CharField(max_length=50, null=True, blank=True)
    user_zipcode = models.CharField(max_length=5, null=True, blank=True)
