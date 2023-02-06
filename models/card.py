from django.db import models
from django.db.models.deletion import CASCADE
from .user import CustomUser


class Card(models.Model):
    card_types = [('Visa', 'Visa'), ('MasterCard', 'MasterCard'),
                  ('AmericanExpress', 'AmericanExpress'), ('Discover', 'Discover')]
    card_id = models.AutoField(primary_key=True)
    card_user = models.ForeignKey(CustomUser, on_delete=CASCADE)
    card_type = models.CharField(max_length=50, choices=card_types)
    card_number = models.CharField(max_length=20, unique=True)
    card_exp_date = models.CharField(max_length=5)
    card_cvv = models.CharField(max_length=5)
    card_billing_zipcode = models.CharField(max_length=5)

    def __str__(self):
        return self.card_id
